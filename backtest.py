import pandas as pd
from compute.compute_returns import compute_returns, compute_trends
from ml.feature_matrix import build_feature_matrix
from ml.predict import load_models, make_predictions
from compute.final_flag_v2 import compute_flag_v2


def run_backtest(df, initial_capital=100_000):
    """
    Backtest בסיסי ל־5 שנים:
    - כניסה/יציאה לפי דגלים
    - מדידת רווח/הפסד
    - Equity Curve
    """

    # חישוב תשואות וטרנדים
    df = compute_returns(df)
    df = compute_trends(df)

    # טעינת מודלים
    model_daily, model_weekly = load_models()

    capital = initial_capital
    position = 0   # 1 = בפנים, 0 = בחוץ
    equity_curve = []

    for i in range(20, len(df)):  # מתחילים אחרי שיש פיצ'רים מלאים
        row = df.iloc[i]

        # פיצ'רים של היום
        features = build_feature_matrix(df.iloc[: i + 1]).tail(1)

        # תחזיות
        pred_1d, pred_5d = make_predictions(model_daily, model_weekly, features)

        # Flags 2.0
        flag, score = compute_flag_v2(
            pred_1d,
            pred_5d,
            row["trend_10d"],
            row["trend_20d"],
            row["ret_1d"]
        )

        # לוגיקת כניסה/יציאה פשוטה
        if flag in ["🔴", "🟠"]:
            position = 0
        else:
            position = 1

        # עדכון הון
        if position == 1 and pd.notna(row["ret_1d"]):
            capital *= (1 + row["ret_1d"])

        equity_curve.append(capital)

    df_bt = pd.DataFrame({
        "date": df.iloc[20:]["date"].values,
        "equity": equity_curve
    })

    return df_bt
