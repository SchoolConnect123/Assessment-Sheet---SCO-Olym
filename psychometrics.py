# app/services/psychometrics.py

import statistics
from typing import List

def consistency_index(metrics: List[float]) -> float:
    """
    metrics: list of differences (student% − class%) across your four charts
    Returns the population standard deviation as a consistency score.
    """
    return statistics.pstdev(metrics)

# If you capture a confidence field, you can add:
# from sklearn.metrics import brier_score_loss
# def calibration_score(y_true: List[int], y_conf: List[float]) -> float:
#     return brier_score_loss(y_true, y_conf)
