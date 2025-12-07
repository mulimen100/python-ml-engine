import pandas as pd
from .advanced_features import build_advanced_features

def build_feature_matrix(df):
    """
    מחזיר מטריצת פיצ'רים משולבת (Feature Matrix 2.0)
    משלבת:
    - פיצ'רים בסיסיים (returns + trends)
    - פיצ'רים מתקדמים (RSI, MACD, Bollinger, Volatility...)
    - rolling windows (אם קיימים בעתיד)
    - סנטימנט (אם יתוסף בעתיד)
    """

    # --- פיצ'רים בסיסיים ---
    base_features = df[[
        "ret_1d",
        "ret_5d",
        "trend_10d",
        "trend_20d"
    ]].copy()

    # --- פיצ'רים מתקדמים ---
    adv = build_advanced_features(df)

    # --- איחוד בסיס + מתקדם ---
    feature_matrix = pd.concat([base_features, adv], axis=1)

    # --- ניקוי ופורמט אחיד ---
    feature_matrix = feature_matrix.fillna(0)

    return feature_matrix
