# app/services/misconception.py
from typing import List, Dict

def most_common_distractor(rows: List[Dict]) -> List[Dict]:
    """
    rows: list of {q_no, your_choice, distractor, freq}
    Returns one entry per question with the top‐freq distractor.
    """
    out = {}
    for r in rows:
        q = r["q_no"]
        freq = r["freq"]
        if q not in out or freq > out[q]["freq"]:
            out[q] = {
                "q_no": q,
                "your_choice": r["your_choice"],
                "distractor": r["distractor"],
                "freq": freq
            }
    return list(out.values())
