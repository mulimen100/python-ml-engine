def build_ml_signal(pred_1d, pred_5d):
    """
    הופך תחזיות לוגיות לסיגנל אחיד.
    """

    if pred_5d == 1:
        return "DOWN_OR_FLAT_5D"
    if pred_1d == 1:
        return "DOWN_OR_FLAT"
    return "UP"
