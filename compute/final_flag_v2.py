def compute_flag_v2(ml_pred_1d, ml_pred_5d, trend_10d, trend_20d, ret_1d):
    """
    Flags 2.0 — שיטת משקולות חכמה:
    - 5D כבד יותר מ־1D
    - טרנדים 20D > 10D
    - penalty על סתירות
    - הפקת confidence רציף (0–100)
    - החזרת דגל סופי
    """

    score = 0.0

    # --- ML Weighting ---
    # 5D = משמעותי יותר
    if ml_pred_5d == 1:
        score += 45
    if ml_pred_1d == 1:
        score += 25

    # --- Trend Weighting ---
    # 20D = כיוון שוק עמוק
    if trend_20d < -0.05:
        score += 20
    elif trend_20d < -0.03:
        score += 12

    # 10D = מגמה קצרה יותר
    if trend_10d < -0.03:
        score += 10
    elif trend_10d < -0.015:
        score += 6

    # --- Daily Return Impact ---
    if ret_1d < -0.01:
        score += 8
    elif ret_1d < -0.005:
        score += 4

    # --- Penalty על סתירות ---
    # למשל ML אומר DOWN אבל טרנדים חיוביים → מורידים ביטחון
    if ml_pred_5d == 1 and trend_20d > 0:
        score -= 10
    if ml_pred_1d == 1 and ret_1d > 0:
        score -= 6

    # ניקוי טווח
    score = max(0, min(score, 100))

    # --- Map score → flag ---
    if score >= 70:
        flag = "🔴"
    elif score >= 45:
        flag = "🟠"
    elif score >= 20:
        flag = "🟡"
    else:
        flag = "🟢"

    return flag, score
