from datetime import datetime
from .export_csv import export_csv, export_json
import pandas as pd
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent


def build_daily_report(date, ml_signal, final_flag, ret_1d, ret_5d, trend_10d, trend_20d):
    """
    יוצר דוח יומי בסיסי – גם CSV וגם JSON
    """

    df = pd.DataFrame([{
        "date": date,
        "ml_signal": ml_signal,
        "final_flag": final_flag,
        "ret_1d": ret_1d,
        "ret_5d": ret_5d,
        "trend_10d": trend_10d,
        "trend_20d": trend_20d
    }])

    csv_path = OUTPUT_DIR / f"daily_report_{date}.csv"
    json_path = OUTPUT_DIR / f"daily_report_{date}.json"

    export_csv(df, str(csv_path))
    export_json(df.to_dict(orient="records"), str(json_path))

    return {
        "csv": str(csv_path),
        "json": str(json_path)
    }


if __name__ == "__main__":
    # === הפקה אמיתית של הדוח ===
    today = datetime.now().strftime("%Y-%m-%d")

    # ערכים לדוגמה עד שיהיו לך נתונים אמיתיים מהמנוע
    ml_signal = "UP"
    final_flag = "🟢"
    ret_1d = 0.003
    ret_5d = 0.012
    trend_10d = 0.015
    trend_20d = 0.025

    result = build_daily_report(
        today,
        ml_signal,
        final_flag,
        ret_1d,
        ret_5d,
        trend_10d,
        trend_20d
    )

    print("נוצר דוח יומי:")
    print(result)

