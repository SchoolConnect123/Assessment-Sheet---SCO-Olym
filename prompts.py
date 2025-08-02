# app/services/prompts.py

"""
Template prompts for GPT‐4o report sections.
Use Python str.format() to inject student and metric data.
"""

# COVER LETTER: polite intro to the student’s performance summary
COVER_LETTER = """
You are an academic counselor at {school_name}. 
Write a brief, upbeat cover letter addressed to {student_name} (Grade {grade}), 
congratulating them on completing their assessment with an overall score of {percentage_score}%. 
Mention one strength and one area for growth, and invite them to review the detailed insights below.
"""

# KEY TAKEAWAYS: bullet out the most important insights from the raw metrics
KEY_TAKEAWAYS = """
You have the following JSON metrics for {student_name}:
{metrics_json}

From these, generate 3–5 concise bullet points (each one sentence) summarizing the key insights about their performance.
"""

# RECOMMENDATIONS: actionable tips based on those same metrics
RECOMMENDATIONS = """
Using the same JSON metrics for {student_name}:
{metrics_json}

Provide 3–5 clear recommendations (each one sentence) to help the student improve in their weaker areas
and build on their strengths.
"""

# STUDY PLAN: a short, structured study plan
STUDY_PLAN = """
Based on the performance metrics for {student_name}:
{metrics_json}

Draft a 1‑week study plan outline. For each day (Day 1 through Day 7), 
suggest a focused activity or topic review (one sentence each).
"""

