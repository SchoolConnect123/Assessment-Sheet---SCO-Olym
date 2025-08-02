# app/services/insights_generator.py

from typing import List, Tuple
from app.services.data_loader import get_questions_df
import pandas as pd


def compute_insights_for_metric(
    metric: str,
    labels: List[str],
    student_vals: List[float],
    class_vals: List[float],
    student_id: str  # ← add this
) -> Tuple[str, str]:
    # load question metadata
    qdf = get_questions_df()
    # load per‐question results from your DB for this student:
    from app.database import get_db_session
    session = next(get_db_session())
    sql = text("""
      SELECT q.[Q.No], q.[Difficulty], q.[Bloom], q.[Skill Type], q.[Chapter Name], r.Score
      FROM questions q
      JOIN results r ON r.[Q.No]=q.[Q.No] AND r.[Student Name]=:student
    """)
    rows = session.execute(sql, {"student": student_id}).mappings().all()
    session.close()
    rdf = pd.DataFrame(rows)

    # now you can for example compute:
    #   medium_pct = rdf[rdf['Difficulty']=='Medium']['Score'].sum() / ( count*MAX_SCORE ) * 100
    #   critical_pct = rdf[rdf['Bloom']=='Critical Thinking']...
    # and add those text snippets to your obs/rec

    # ... then fall back to your existing logic below


def _pct(v: float) -> str:
    return f"{v:.1f}%"

def _top_n(indices, n=2):
    return indices[:n]

def compute_insights_for_metric(
    metric: str,
    labels: List[str],
    student_vals: List[float],
    class_vals: List[float],
) -> Tuple[str, str]:
    """
    Build human-readable Observation & Recommendation strings for one metric
    (difficulty, bloom, skill, chapter) using the already aggregated chart data.
    Nothing is read from DB or Excel here, so it's safe & fast.
    """

    # No data
    if not labels:
        return ("No data available to analyse.", "No recommendation available.")

    # Overall compare
    stu_avg = sum(student_vals) / len(student_vals)
    cls_avg = sum(class_vals)   / len(class_vals)
    gap     = stu_avg - cls_avg

    if gap >= 0:
        overall = (
            f"Overall the student is **above** the class average "
            f"({_pct(stu_avg)} vs {_pct(cls_avg)}; +{_pct(abs(gap))})."
        )
    else:
        overall = (
            f"Overall the student is **below** the class average "
            f"({_pct(stu_avg)} vs {_pct(cls_avg)}; -{_pct(abs(gap))})."
        )

    # Strengths / weaknesses by category
    # (diff = student - class)
    diffs = [sv - cv for sv, cv in zip(student_vals, class_vals)]
    # descending indices by diff
    sorted_idx = sorted(range(len(diffs)), key=lambda i: diffs[i], reverse=True)

    strengths_idx  = [i for i in sorted_idx if diffs[i] >  5]  # > +5% above class
    weaknesses_idx = [i for i in sorted_idx[::-1] if diffs[i] < -5]  # > -5% below class

    strengths_txt = ""
    weaknesses_txt = ""
    if strengths_idx:
        top = _top_n(strengths_idx, 2)
        strengths_txt = ", ".join([f"{labels[i]} ({_pct(student_vals[i])})" for i in top])

    if weaknesses_idx:
        topw = _top_n(weaknesses_idx, 2)
        weaknesses_txt = ", ".join([f"{labels[i]} ({_pct(student_vals[i])})" for i in topw])

    # < 50% buckets
    under_50 = [labels[i] for i, sv in enumerate(student_vals) if sv < 50.0]
    zero_pct = [labels[i] for i, sv in enumerate(student_vals) if sv == 0.0]

    # Metric‑specific nuggets
    extras = []
    metric_l = metric.lower()
    if metric_l == "difficulty":
        # try to detect 'Medium' weakness
        if "Medium" in labels:
            i = labels.index("Medium")
            if student_vals[i] < 50:
                extras.append(f"Medium-difficulty questions are weak ({_pct(student_vals[i])}).")
    elif metric_l == "bloom":
        for high in ("Analyze", "Evaluation", "Create", "Evaluate"):
            if high in labels:
                j = labels.index(high)
                if student_vals[j] < cls_avg:
                    extras.append(f"Lower performance in higher-order thinking ({high}: {_pct(student_vals[j])}).")
    elif metric_l == "skill":
        # call out very low skill buckets
        very_low = [labels[i] for i, sv in enumerate(student_vals) if sv < 30]
        if very_low:
            extras.append(f"Very low scores in: {', '.join(very_low)}.")
    elif metric_l == "chapter":
        if zero_pct:
            extras.append(f"{len(zero_pct)} chapter(s) at 0%: {', '.join(zero_pct[:3])}{'…' if len(zero_pct) > 3 else ''}.")

    # Compose Observation
    observation_parts = [overall]
    if strengths_txt:
        observation_parts.append(f"Strongest {metric} area(s): **{strengths_txt}**.")
    if weaknesses_txt:
        observation_parts.append(f"Weakest {metric} area(s): **{weaknesses_txt}**.")
    if under_50:
        observation_parts.append(f"Below 50% in: {', '.join(under_50[:3])}{'…' if len(under_50) > 3 else ''}.")
    if extras:
        observation_parts.append(" ".join(extras))

    observation = " ".join(observation_parts)

    # Compose Recommendation (focus primarily on weaknesses)
    rec_parts = []
    if weaknesses_txt:
        rec_parts.append(
            f"Prioritize **{weaknesses_txt}**; revise core concepts and practice targeted questions."
        )
    if metric_l == "difficulty" and "Medium" in labels:
        i = labels.index("Medium")
        if student_vals[i] < 50:
            rec_parts.append("Spend extra time on **Medium-difficulty** items to improve consistency.")
    if metric_l == "bloom":
        rec_parts.append("Include more higher-order Bloom-level practice (Analyze/Evaluate/Create).")
    if zero_pct and metric_l == "chapter":
        rec_parts.append(
            f"Start fixing the 0% chapters first: {', '.join(zero_pct[:3])}{'…' if len(zero_pct) > 3 else ''}."
        )
    if not rec_parts:
        rec_parts.append(f"Maintain performance but aim to close the {_pct(abs(gap))} gap to the class average.")

    recommendation = " ".join(rec_parts)

    return observation, recommendation
