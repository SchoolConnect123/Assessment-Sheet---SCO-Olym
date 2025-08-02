# app/services/chart_generator.py

import os
import logging
from typing import Dict, List, Tuple
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.ioff()

from sqlalchemy import text
from app.database import get_db_session
from app.services.insights_generator import compute_insights_for_metric

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.getcwd(), "app", "static", "charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_SCORE = 3

PALETTE = {
    "difficulty": {"student": "#0d6efd", "class": "#198754"},
    "bloom":      {"student": "#0d6efd", "class": "#198754"},
    "skill":      {"student": "#6f42c1", "class": "#20c997"},
    "chapter":    {"student": "#6f42c1", "class": "#20c997"},
}

QUERIES: Dict[str, str] = {
    "difficulty": f"""
        SELECT q.[Difficulty] AS category,
               SUM(r.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS student_val,
               SUM(r2.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS class_val
        FROM questions q
        JOIN results r  ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        JOIN results r2 ON r2.[Q.No]=q.[Q.No]
        GROUP BY q.[Difficulty]
    """,
    "bloom": f"""
        SELECT q.[Bloom] AS category,
               SUM(r.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS student_val,
               SUM(r2.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS class_val
        FROM questions q
        JOIN results r  ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        JOIN results r2 ON r2.[Q.No]=q.[Q.No]
        GROUP BY q.[Bloom]
    """,
    "skill": f"""
        SELECT q.[Skill Type] AS category,
               SUM(r.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS student_val,
               SUM(r2.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS class_val
        FROM questions q
        JOIN results r  ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        JOIN results r2 ON r2.[Q.No]=q.[Q.No]
        GROUP BY q.[Skill Type]
    """,
    "chapter": f"""
        SELECT q.[Chapter Name] AS category,
               SUM(r.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS student_val,
               SUM(r2.Score)*100.0/(COUNT(*)*{MAX_SCORE}) AS class_val
        FROM questions q
        JOIN results r  ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
        JOIN results r2 ON r2.[Q.No]=q.[Q.No]
        GROUP BY q.[Chapter Name]
    """,
}

DESCRIPTIONS = {
    "difficulty": "Difficulty analysis highlights which questions were easy or hard, guiding targeted practice.",
    "bloom":      "Bloom's taxonomy analysis shows the cognitive skills (Remember, Apply, Analyze) where improvement is needed.",
    "skill":      "Skill-based analysis highlights specific mathematical or logical skills that require attention.",
    "chapter":    "Chapter-wise analysis helps focus on chapters where the student can improve the most."
}


def _run_query(db, metric: str, student_id: str) -> Tuple[List[str], List[float], List[float]]:
    sql = text(QUERIES[metric])
    rows = db.execute(sql, {"student": student_id}).mappings().all()
    labels       = [r["category"] for r in rows]
    student_vals = [float(r["student_val"]) for r in rows]
    class_vals   = [float(r["class_val"]) for r in rows]
    return labels, student_vals, class_vals


def _render_chart(student_id: str, metric: str,
                  labels: List[str],
                  student_vals: List[float],
                  class_vals: List[float]) -> str:
    filename = f"{student_id}_{metric}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    colors = PALETTE[metric]

    if metric in ("skill", "chapter"):
        fig, ax = plt.subplots(figsize=(8, len(labels) * 0.3 + 2))
        y = list(range(len(labels)))
        ax.barh([i - 0.2 for i in y], student_vals, height=0.4, label="Student", color=colors["student"])
        ax.barh([i + 0.2 for i in y], class_vals,   height=0.4, label="Class",   color=colors["class"])
        ax.set_yticks(y)
        ax.set_yticklabels(labels)
        ax.set_xlabel("% Score")
        ax.set_title(f"{metric.title()} (%)")
        ax.set_xlim(0, 100)
        ax.legend()
        for i, v in enumerate(student_vals):
            ax.text(v + 1, i - 0.25, f"{v:.1f}%", va="center", fontsize=8)
        for i, v in enumerate(class_vals):
            ax.text(v + 1, i + 0.05, f"{v:.1f}%", va="center", fontsize=8)
    else:
        fig, ax = plt.subplots(figsize=(6, 4))
        x = list(range(len(labels)))
        ax.bar([i - 0.2 for i in x], student_vals, width=0.4, label="Student", color=colors["student"])
        ax.bar([i + 0.2 for i in x], class_vals,   width=0.4, label="Class",   color=colors["class"])
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=0, ha="center")
        ax.set_ylabel("% Score")
        ax.set_title(f"{metric.title()} (%)")
        ax.set_ylim(0, 100)
        ax.legend()
        for i, v in enumerate(student_vals):
            ax.text(i - 0.25, v + 1, f"{v:.1f}%", fontsize=8)
        for i, v in enumerate(class_vals):
            ax.text(i + 0.05, v + 1, f"{v:.1f}%", fontsize=8)

    fig.tight_layout()
    fig.savefig(filepath, bbox_inches="tight")
    plt.close(fig)

    return f"/static/charts/{filename}"


def generate_all_charts(student_id: str) -> Dict[str, Dict]:
    """
    Returns a dict keyed by metric with 'observation' & 'recommendation'
    added so your template can show them directly.
    """
    session = next(get_db_session())
    try:
        results: Dict[str, Dict] = {}
        for metric in QUERIES:
            labels, s_vals, c_vals = _run_query(session, metric, student_id)

            if labels:
                url = _render_chart(student_id, metric, labels, s_vals, c_vals)
            else:
                url = f"/static/charts/{student_id}_{metric}.png"

            # <<< NEW: Compute insight text >>>
            obs, rec = compute_insights_for_metric(metric, labels, s_vals, c_vals)
            

            results[metric] = {
                "title":          metric.title(),
                "url":            url,
                "labels":         labels,
                "student_values": [round(v, 1) for v in s_vals],
                "class_values":   [round(v, 1) for v in c_vals],
                "description":    DESCRIPTIONS.get(metric, ""),
                "observation":     obs,
                "recommendation":  rec,
            }

        return results
    finally:
        session.close()
