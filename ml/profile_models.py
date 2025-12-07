import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from .feature_matrix import build_feature_matrix


def build_profile_dataset(df_profile):
    """
    יוצר dataset פרופילי:
    - פיצ'רים פרופיליים (Feature Matrix 2.0)
    - יעד 1D ו־5D לפי תשואות אמיתיות של הפרופיל
    """
    features = build_feature_matrix(df_profile)

    # יעדים: תשואה שלילית = 1, חיובית/ניטרלית = 0
    target_1d = (df_profile["ret_1d"] < 0).astype(int)
    target_5d = (df_profile["ret_5d"] < 0).astype(int)

    return features, target_1d, target_5d


def train_profile_models(profile_id, df_profile):
    """
    מאמן שני מודלים ייעודיים לפרופיל:
    - model_<profile_id>_daily.pkl
    - model_<profile_id>_weekly.pkl
    """

    features, t1d, t5d = build_profile_dataset(df_profile)

    model_daily = RandomForestClassifier()
    model_daily.fit(features, t1d)

    model_weekly = RandomForestClassifier()
    model_weekly.fit(features, t5d)

    # שמות מודלים דינמיים לפי profile_id
    daily_path = f"../ml/model_{profile_id}_daily.pkl"
    weekly_path = f"../ml/model_{profile_id}_weekly.pkl"

    joblib.dump(model_daily, daily_path)
    joblib.dump(model_weekly, weekly_path)

    return daily_path, weekly_path


def load_profile_models(profile_id):
    """
    טוען את המודלים הייעודיים של הפרופיל.
    """

    daily_path = f"../ml/model_{profile_id}_daily.pkl"
    weekly_path = f"../ml/model_{profile_id}_weekly.pkl"

    model_daily = joblib.load(daily_path)
    model_weekly = joblib.load(weekly_path)

    return model_daily, model_weekly
