# app/services/report_generator.py

import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.report import GPTReport as GPTReportSchema
from app.services.prompts import COVER_LETTER, KEY_TAKEAWAYS, RECOMMENDATIONS, STUDY_PLAN
from app.gpt_utils import client
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session



def generate_full_report(student_data: dict, db) -> GPTReportSchema:
    student_id = student_data["id"]

    # --- Fetch core metrics (always needed for grade & score) ---
    metrics = db.execute(
        text(
            "SELECT CAST(Grade AS varchar(10)) AS grade, "
            "REPLACE([Percentage Score], '%', '') AS percentage_score "
            "FROM summary WHERE [Name] = :name"
        ),
        {"name": student_id}
    ).mappings().one_or_none()

    if not metrics:
        # Student not found in summary
        return GPTReportSchema(
            student_id=student_id,
            grade="N/A",
            percentage_score=0.0,
            cover_letter=f"[FALLBACK] Cover Letter for {student_id}",
            key_takeaways=f"[FALLBACK] Key Takeaways for {student_id}",
            recommendations=f"[FALLBACK] Recommendations for {student_id}",
            study_plan=f"[FALLBACK] Study Plan for {student_id}",
        )

    grade = metrics["grade"] or "N/A"
    percentage_score = float(metrics["percentage_score"] or 0.0)

    # --- Check cache in reports table ---
    try:
        row = db.execute(
            text(
                "SELECT cover_letter, key_takeaways, recommendations, study_plan "
                "FROM reports WHERE student_id = :id"
            ),
            {"id": student_id}
        ).fetchone()
    except SQLAlchemyError:
        row = None

    if row:
        return GPTReportSchema(
            student_id=student_id,
            grade=grade,
            percentage_score=percentage_score,
            cover_letter=row.cover_letter,
            key_takeaways=row.key_takeaways,
            recommendations=row.recommendations,
            study_plan=row.study_plan,
        )

    # --- Prepare prompts ---
    detailed = {
        "difficulty": {"student": [], "class": []},
        "bloom":      {"student": [], "class": []},
        "skill":      {"student": [], "class": []},
        "chapter":    {"student": [], "class": []},
    }
    metrics_json = json.dumps(detailed)

    prompts = {
        "cover_letter": COVER_LETTER.format(
            school_name=student_data.get("school", "Your School"),
            student_name=student_id,
            grade=grade,
            percentage_score=percentage_score,
        ),
        "key_takeaways": KEY_TAKEAWAYS.format(
            student_name=student_id,
            metrics_json=metrics_json,
        ),
        "recommendations": RECOMMENDATIONS.format(
            student_name=student_id,
            metrics_json=metrics_json,
        ),
        "study_plan": STUDY_PLAN.format(
            student_name=student_id,
            metrics_json=metrics_json,
        ),
    }

    # --- Generate GPT sections ---
    sections = {}
    for key, prompt in prompts.items():
        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            sections[key] = resp.choices[0].message.content
        except Exception:
            sections[key] = f"[FALLBACK] {key.replace('_', ' ').title()} for {student_id}"

    # --- Cache result ---
    now = datetime.utcnow()
    try:
        db.execute(
            text(
                "INSERT INTO reports "
                "(student_id, cover_letter, key_takeaways, recommendations, study_plan, created_at, updated_at) "
                "VALUES (:id, :cv, :kt, :rc, :sp, :now, :now)"
            ),
            {
                "id": student_id,
                "cv": sections["cover_letter"],
                "kt": sections["key_takeaways"],
                "rc": sections["recommendations"],
                "sp": sections["study_plan"],
                "now": now,
            }
        )
        db.commit()
    except SQLAlchemyError:
        pass

    return GPTReportSchema(
        student_id=student_id,
        grade=grade,
        percentage_score=percentage_score,
        cover_letter=sections["cover_letter"],
        key_takeaways=sections["key_takeaways"],
        recommendations=sections["recommendations"],
        study_plan=sections["study_plan"],
    )


def compute_skill_summary(student_id: str, db: Session) -> list[dict]:
    rows = db.execute(text("""
        SELECT
          q.[Skill Type] AS skill,
          SUM(CASE WHEN r.Status='Correct' THEN 1 ELSE 0 END) AS correct,
          COUNT(*) AS total
        FROM questions q
        JOIN results r ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        GROUP BY q.[Skill Type]
    """), {"student": student_id}).mappings().all()

    summary = []
    for row in rows:
        skill = row["skill"]
        correct = row["correct"]
        total = row["total"]
        incorrect = total - correct
        accuracy = (correct / total * 100) if total else 0.0

        # pull up to 3 example question numbers/text for correct & incorrect
        def examples(status, limit=3):
            q = text(f"""
                SELECT TOP {limit}
                  q.[Q.No] AS q_no, q.Question AS question_text
                FROM questions q
                JOIN results r ON r.[Q.No]=q.[Q.No]
                WHERE r.[Student Name]=:student
                  AND q.[Skill Type]=:skill
                  AND r.Status {'=' if status=='Correct' else '<>'} 'Correct'
            """)
            return [
                f"Q{r['q_no']} “{r['question_text']}”"
                for r in db.execute(q, {"student": student_id, "skill": skill}).mappings().all()
            ]

        summary.append({
            "skill": skill,
            "correct": correct,
            "total": total,
            "incorrect": incorrect,
            "accuracy": round(accuracy,1),
            "correct_examples": examples("Correct"),
            "incorrect_examples": examples("Incorrect"),
        })
    return summary


def compute_chapter_summary(student_id: str, db: Session) -> dict:
    rows = db.execute(text("""
        SELECT
          q.[Chapter Name] AS chapter,
          AVG(CASE WHEN r.Score>0 THEN 1.0 ELSE 0 END)*100.0 AS pct,
          STRING_AGG(CONCAT('Q',q.[Q.No]),',') AS qlist
        FROM questions q
        JOIN results r ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        GROUP BY q.[Chapter Name]
    """), {"student": student_id}).mappings().all()

    strengths, weaknesses, low_mod = [], [], []
    for r in rows:
        ch, pct, ql = r["chapter"], float(r["pct"]), r["qlist"]
        if pct == 100:
            strengths.append(f"{ch} ({ql})")
        elif pct == 0:
            weaknesses.append(f"{ch} ({ql})")
        elif pct <= 50:
            low_mod.append(f"{ch} ({ql}) – {pct:.0f}%")
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "low_to_moderate": low_mod
    }

