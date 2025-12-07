def resolve_conflict(ml_pred_1d, ml_pred_5d, volatility_20d, score_1d, score_5d):
    """
    Conflict Resolver 2.0
    - אם 1D UP ו-5D DOWN → בודקים היסטוריה, תנודתיות ומשקולות
    """

    # ברירת מחדל — הנחה: 5D חשוב יותר
    decision = "5D"
    confidence = 0

    # 1) 5D DOWN ו-1D UP → conflict ראשי
    conflict = (ml_pred_1d == 0 and ml_pred_5d == 1)

    if not conflict:
        return "NO_CONFLICT", 0

    # 2) תנודתיות גבוהה → 5D מקבל עדיפות
    if volatility_20d > 0.02:
        decision = "5D"
        confidence += 40

    # 3) תנודתיות נמוכה → 1D רלוונטי יותר
    elif volatility_20d < 0.01:
        decision = "1D"
        confidence += 35

    # 4) בדיקת "Risk Tilt" לפי חוזק הסיגנל
    if score_5d > score_1d:
        decision = "5D"
        confidence += 25
    else:
        decision = "1D"
        confidence += 25

    # 5) ניקוי טווח
    confidence = max(0, min(confidence, 100))

    return decision, confidence
