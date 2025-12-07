from pathlib import Path
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# בסיס התיקייה של הפרויקט (PY_ENGINE)
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

app = FastAPI(title="Python Engine Local API", version="1.0")


class TodayResponse(BaseModel):
    date: str
    ml_signal: str
    final_flag: str
    ret_1d: float
    ret_5d: float
    trend_10d: float
    trend_20d: float


def _load_today_row() -> pd.Series:
    """
    טוען את שורת היום מתוך daily_report_YYYY-MM-DD.csv
    מניח שקובץ כזה נוצר ע"י build_daily_report.
    """

    today_str = date.today().strftime("%Y-%m-%d")
    csv_path = OUTPUT_DIR / f"daily_report_{today_str}.csv"

    if not csv_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"לא נמצא דוח יומי להיום: {csv_path.name}. ודא שהסקריפט daily_report רץ."
        )

    df = pd.read_csv(csv_path)

    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="קובץ הדוח היומי ריק."
        )

    # לוקחים את השורה הראשונה (מניח דוח אחד ביום)
    return df.iloc[0]


@app.get("/health")
def health_check():
    """
    בדיקת חיים בסיסית ל-API.
    """
    return {"status": "ok"}


@app.get("/today", response_model=TodayResponse)
def get_today_status():
    """
    מחזיר:
    - ML_SIGNAL
    - FINAL_FLAG
    - כל הנתונים המספריים של היום (ret/trend)
    מתוך קובץ daily_report_YYYY-MM-DD.csv
    """

    row = _load_today_row()

    # חשוב: שמות העמודות צריכים להתאים לדוח שכתבת ב-daily_report.py
    try:
        return TodayResponse(
            date=str(row["date"]),
            ml_signal=str(row["ml_signal"]),
            final_flag=str(row["final_flag"]),
            ret_1d=float(row["ret_1d"]),
            ret_5d=float(row["ret_5d"]),
            trend_10d=float(row["trend_10d"]),
            trend_20d=float(row["trend_20d"]),
        )
    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"חסרה עמודה בדוח היומי: {e}. ודא ששמות העמודות בדוח תואמים."
        )


@app.get("/signal")
def get_today_signal():
    """
    מחזיר רק את ה-ML_SIGNAL וה-FINAL_FLAG של היום.
    שימושי לאינטגרציה פשוטה.
    """
    row = _load_today_row()
    return {
        "date": str(row.get("date", "")),
        "ml_signal": str(row.get("ml_signal", "")),
        "final_flag": str(row.get("final_flag", "")),
    }
