def compute_basic_flag(row):
    """
    שיחזור לוגיקה בסיסית של הדגל (לא ML)
    לדוגמה בלבד – בהמשך נעדכן לוגיקה מלאה.
    """

    if row["trend_20d"] < -0.05:
        return "🔴"
    if row["trend_10d"] < -0.03:
        return "🟠"
    if row["ret_1d"] < -0.01:
        return "🟡"
    return "🟢"
