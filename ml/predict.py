import joblib

def load_models():
    daily = joblib.load("../ml/model_daily.pkl")
    weekly = joblib.load("../ml/model_weekly.pkl")
    return daily, weekly

def make_predictions(model_daily, model_weekly, features_today):
    pred_1d = model_daily.predict(features_today)[0]
    pred_5d = model_weekly.predict(features_today)[0]
    return pred_1d, pred_5d
