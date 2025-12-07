import pandas as pd

def compute_trends(df):
    """
    מחשב טרנדים 10D ו-20D על close_value
    """
    df = df.copy()
    df["trend_10d"] = df["close_value"].pct_change(10)
    df["trend_20d"] = df["close_value"].pct_change(20)
    return df
