def combine_flag(ml_signal, row):
    """
    מחזיר דגל סופי 🟢🟡🟠🔴
    שילוב של:
    - ML_SIGNAL
    - טרנדים 10D/20D
    - תשואות 1D/5D
    """

    # 1) ML חזק קודם כל
    if ml_signal == "DOWN_OR_FLAT_5D":
        return "🔴"
    if ml_signal == "DOWN_OR_FLAT":
        return "🟠"

    # 2) טרנדים שליליים משמעותיים
    if row.get("trend_20d", 0) < -0.05:
        return "🔴"
    if row.get("trend_10d", 0) < -0.03:
        return "🟠"

    # 3) תשואה יומית חלשה
    if row.get("ret_1d", 0) < -0.01:
        return "🟡"

    # 4) ברירת מחדל — מצב תקין
    return "🟢"
