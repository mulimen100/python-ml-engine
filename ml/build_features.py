import pandas as pd

def build_features(df):
    """
    יוצר פיצ'רים ל-ML מתוך DataFrame מוכן.
    מניח שקיימים:
    ret_1d, ret_5d, trend_10d, trend_20d
    """

    df = df.copy()

    features = df[[
        "ret_1d",
        "ret_5d",
        "trend_10d",
        "trend_20d"
    ]].fillna(0)

    return features
