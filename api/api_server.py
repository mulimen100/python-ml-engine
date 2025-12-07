from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Python Engine Local & Cloud API", version="2.0")


class TodayResponse(BaseModel):
    date: str
    ml_signal: str
    final_flag: str
    ret_1d: float
    ret_5d: float
    trend_10d: float
    trend_20d: float


def build_daily_status_live() -> TodayResponse:
    """
    גרסת LIVE פשוטה:
    כרגע מחזירה ערכים דומים למה שהגדרנו ב-daily_report.py.
    בהמשך אפשר לחבר כאן את כל המנוע (ML, Flags, Backtest וכו').
    """

    today = datetime.now().strftime("%Y-%m-%d")

    # TODO: להחליף בהמשך לערכים אמיתיים מהמנוע
    ml_signal = "UP"
    final_flag = "🟢"
    ret_1d = 0.003
    ret_5d = 0.012
    trend_10d = 0.015
    trend_20d = 0.025

    return TodayResponse(
        date=today,
        ml_signal=ml_signal,
        final_flag=final_flag,
        ret_1d=ret_1d,
        ret_5d=ret_5d,
        trend_10d=trend_10d,
        trend_20d=trend_20d,
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/today", response_model=TodayResponse)
def get_today_status():
    """
    דוח LIVE – מחושב בזמן אמת, בלי לקרוא שום קובץ.
    """
    return build_daily_status_live()


@app.get("/signal")
def get_today_signal():
    """
    אותו מידע כמו /today אבל רק הסיגנל והדגל.
    """
    today_status = build_daily_status_live()
    return {
        "date": today_status.date,
        "ml_signal": today_status.ml_signal,
        "final_flag": today_status.final_flag,
    }
