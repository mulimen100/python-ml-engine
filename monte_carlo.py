import numpy as np
import pandas as pd

def max_drawdown(equity_curve):
    """
    מחשב מקסימום Drawdown למסלול הוני.
    """
    peak = equity_curve[0]
    dd = 0
    for x in equity_curve:
        peak = max(peak, x)
        dd = min(dd, x - peak)
    return abs(dd / peak)


def monte_carlo_simulation(returns, n_sims=500, days=252):
    """
    סימולציית Monte Carlo:
    - returns: סדרת ret_1d היסטורית
    - n_sims: כמות סימולציות
    - days: כמה ימים קדימה לסמלץ (252 ~= שנה)
    """

    sims_dd = []

    for _ in range(n_sims):
        # דגימה אקראית מתשואות היסטוריות
        sampled = np.random.choice(returns, size=days, replace=True)

        # בניית עקומת הון
        equity = [1]
        for r in sampled:
            equity.append(equity[-1] * (1 + r))

        # חישוב drawdown
        dd = max_drawdown(equity)
        sims_dd.append(dd)

    # התפלגות Drawdowns
    dd_series = pd.Series(sims_dd)

    # מדד סיכון – לדוגמה: P95 drawdown
    risk_score = dd_series.quantile(0.95)

    return {
        "drawdown_distribution": dd_series,
        "risk_score": risk_score
    }
