import joblib
from sklearn.ensemble import RandomForestClassifier

def train_models(features, target_1d, target_5d):
    """
    מאמן שני מודלים:
    model_daily.pkl
    model_weekly.pkl
    """

    model_daily = RandomForestClassifier()
    model_daily.fit(features, target_1d)

    model_weekly = RandomForestClassifier()
    model_weekly.fit(features, target_5d)

    joblib.dump(model_daily, "../ml/model_daily.pkl")
    joblib.dump(model_weekly, "../ml/model_weekly.pkl")

    return model_daily, model_weekly
