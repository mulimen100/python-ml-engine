import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score

LOG_PATH = "../output/calibration_log.csv"

def evaluate_calibration():
    """
    מחשב דיוק ואחוזי פגיעה על בסיס היומן של 6 חודשים.
    """

    df = pd.read_csv(LOG_PATH)

    # מודל יומי
    y_true_1d = (df["real_ret_1d"] < 0).astype(int)
    y_pred_1d = df["ml_pred_1d"]

    acc_1d = accuracy_score(y_true_1d, y_pred_1d)
    cm_1d = confusion_matrix(y_true_1d, y_pred_1d)

    # מודל שבועי
    y_true_5d = (df["real_ret_5d"] < 0).astype(int)
    y_pred_5d = df["ml_pred_5d"]

    acc_5d = accuracy_score(y_true_5d, y_pred_5d)
    cm_5d = confusion_matrix(y_true_5d, y_pred_5d)

    return {
        "accuracy_1d": acc_1d,
        "confusion_1d": cm_1d.tolist(),
        "accuracy_5d": acc_5d,
        "confusion_5d": cm_5d.tolist()
    }
