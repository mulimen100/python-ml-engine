import pandas as pd

def compute_returns(df):
    """
    מקבל DataFrame עם עמודת close_value
    מחזיר df עם 1D ו-5D
    """
    df = df.copy()
    df["ret_1d"] = df["close_value"].pct_change()
    df["ret_5d"] = df["close_value"].pct_change(5)
    return df
