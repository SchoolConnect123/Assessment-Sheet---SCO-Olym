# app/services/irt.py
import math
from sqlalchemy import text
from app.database import get_db_session  # or however you get a Session

def question_params(db):
    """
    Return a dict mapping each question number to its difficulty b
    (b = –ln(p/(1–p))), where p is the fraction of students who scored >0.
    """

    rows = db.execute(
        text("""
            SELECT
              [Q.No]          AS q_no,
              AVG(CASE WHEN Score > 0 THEN 1.0 ELSE 0 END) AS p
            FROM results
            GROUP BY [Q.No]
        """)
    ).mappings().all()

    params = {}
    for r in rows:
        p = float(r["p"])
        # avoid division by zero
        denom = max(1e-9, 1.0 - p)
        b = -math.log(p / denom + 1e-9)
        params[r["q_no"]] = b

    return params

def estimate_ability(responses, bs):
    """
    responses: list of (q_no, correct:0/1)
    bs: dict of {q_no: difficulty}
    We'll do a very simple Newton–Raphson to find θ solving sum(u_i – P_i(θ)) = 0
    """
    # initial guess
    theta = 0.0
    for _ in range(10):
        num = 0.0
        den = 0.0
        for q_no, u in responses:
            b = bs.get(q_no, 0)
            # 1PL model P_i(θ) = 1 / (1 + exp(−(θ−b)))
            exp_term = math.exp(-(theta - b))
            p_i = 1.0 / (1.0 + exp_term)
            num += (u - p_i)
            den += p_i * (1.0 - p_i)
        if den == 0:
            break
        theta += num / den
    return theta

def plot_irt_curve(theta, bs, out_path):
    """
    Generate a curve of P(θ) vs b, save to PNG at out_path.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bs_items = sorted(bs.items(), key=lambda kv: kv[1])
    difficulties = [b for _, b in bs_items]
    probs = [1.0 / (1.0 + math.exp(-(theta - b))) for b in difficulties]

    plt.figure(figsize=(6,4))
    plt.plot(difficulties, probs, marker='o')
    plt.xlabel("Question Difficulty (b)")
    plt.ylabel("P(correct)")
    plt.title(f"IRT Curve (θ = {theta:.2f})")
    plt.ylim(0,1)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
