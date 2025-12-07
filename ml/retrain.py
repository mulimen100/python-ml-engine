import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from .feature_matrix import build_feature_matrix

CALIB_LOG = "../output/calibration_log.csv"

def load_calibration_data():
    """
    טוען את calibration_log ומכין תוצאות אמת:
    real_ret_1d < 0  ==> 1
    real_ret_5d < 0  ==> 1
    """
    df = pd.read_csv(CALIB_LOG)
    df["target_1d"] = (df["real_ret_1d"] < 0).astype(int)
    df["target_5d"] = (df["real_ret_5d"] < 0).astype(int)
    return df


def build_retrain_dataset(snapshot_df, calib_df):
    """
    יוצר דאטסט חדש לאימון:
    - פיצ'רים מתקדמים (Feature Matrix 2.0)
    - תוצאות אמת מה-calibration_log
    """
    features = build_feature_matrix(snapshot_df).reset_index(drop=True)

    # התאמה: נניח שאורך snapshot מתאים לאורך calibration
    # (בפרקטיקה: תוחל גזירה לפי תאריכים)
    targets_1d = calib_df["target_1d"]
    targets_5d = calib_df["target_5d"]

    return features, targets_1d, targets_5d


def retrain_models(features, target_1d, target_5d):
    """
    מאמן שני מודלים חדשים V2
    """

    model_daily_v2 = RandomForestClassifier()
    model_daily_v2.fit(features, target_1d)

    model_weekly_v2 = RandomForestClassifier()
    model_weekly_v2.fit(features, target_5d)

    joblib.dump(model_daily_v2, "../ml/model_daily_v2.pkl")
    joblib.dump(model_weekly_v2, "../ml/model_weekly_v2.pkl")

    return model_daily_v2, model_weekly_v2


def run_retrain(snapshot_df):
    """
    הפונקציה הראשית — מבצעת תהליך Re-Train חצי אוטומטי.
    """

    calib_df = load_calibration_data()
    features, t1d, t5d = build_retrain_dataset(snapshot_df, calib_df)
    return retrain_models(features, t1d, t5d)
