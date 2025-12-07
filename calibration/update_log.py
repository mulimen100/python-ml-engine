import pandas as pd
import os

LOG_PATH = "../output/calibration_log.csv"

def update_calibration_log(date, ml_pred_1d, ml_pred_5d, final_flag, real_ret_1d, real_ret_5d):
    """
    מוסיף שורה חדשה ללוג הכיול.
    """

    new_row = {
        "date": date,
        "ml_pred_1d": ml_pred_1d,
        "ml_pred_5d": ml_pred_5d,
        "final_flag": final_flag,
        "real_ret_1d": real_ret_1d,
        "real_ret_5d": real_ret_5d
    }

    # אם הקובץ עדיין לא קיים → צור חדש
    if not os.path.exists(LOG_PATH):
        df = pd.DataFrame([new_row])
        df.to_csv(LOG_PATH, index=False)
        return df

    # אם קיים → הכנס שורה
    df = pd.read_csv(LOG_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)
    return df
