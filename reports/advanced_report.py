import datetime
import os
from pathlib import Path

from visuals.charts import (
    plot_flags,
    plot_hit_ratio,
    plot_confusion_matrix,
    plot_predictions
)


TEMPLATE = """
<html>
<head>
  <meta charset="utf-8">
  <title>Daily Report - {profile_id}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    h1 {{ font-size: 24px; margin-bottom: 4px; }}
    h2 {{ font-size: 18px; margin-top: 24px; }}
    .section {{ margin-bottom: 26px; }}
    .flag {{ font-size: 32px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 8px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 8px; font-size: 13px; text-align: right; }}
    th {{ background: #f2f2f2; }}
    .small {{ font-size: 11px; color: #666; }}
  </style>
</head>
<body>
  <h1>דוח יומי – {profile_id}</h1>
  <div class="small">תאריך הפקה: {generated_at}</div>

  <div class="section">
    <h2>סטטוס כללי</h2>
    <p>
      דגל סופי: <span class="flag">{final_flag}</span><br>
      Confidence: {confidence:.1f} / 100<br>
      ML 1D: {ml_pred_1d} &nbsp; | &nbsp; ML 5D: {ml_pred_5d}<br>
      Conflict Resolver: {conflict_resolution} (conf={conflict_confidence:.1f})
    </p>
  </div>

  <div class="section">
    <h2>תשואות וטרנדים</h2>
    <table>
      <tr>
        <th>ret 1D</th>
        <th>ret 5D</th>
        <th>trend 10D</th>
        <th>trend 20D</th>
      </tr>
      <tr>
        <td>{ret_1d:.4f}</td>
        <td>{ret_5d:.4f}</td>
        <td>{trend_10d:.4f}</td>
        <td>{trend_20d:.4f}</td>
      </tr>
    </table>
  </div>

  <div class="section">
    <h2>Backtest – Equity Curve (סיכום)</h2>
    <p class="small">
      הון התחלתי: {initial_capital:,.0f}<br>
      הון סופי: {final_equity:,.0f}<br>
      תשואה מצטברת: {total_return:.2%}
    </p>
  </div>

  <div class="section">
    <h2>Monte Carlo – הערכת סיכון</h2>
    <p class="small">
      Risk Score (95% Drawdown): {risk_score:.2%}
    </p>
  </div>

  <div class="section">
    <h2>גרף תנועת דגלים</h2>
    <img src="{img_flags}" width="800">
  </div>

  <div class="section">
    <h2>Hit Ratio (30D)</h2>
    <img src="{img_hit_ratio}" width="800">
  </div>

  <div class="section">
    <h2>Confusion Matrix</h2>
    <img src="{img_confusion}" width="400">
  </div>

  <div class="section">
    <h2>תחזיות 1D / 5D לאורך זמן</h2>
    <img src="{img_predictions}" width="800">
  </div>

</body>
</html>
"""


def build_advanced_report(output_dir,
                          profile_summary: dict,
                          backtest_summary: dict,
                          risk_score: float):
    """
    יוצר קובץ HTML מתקדם למשתמש אחד.
    כולל תמונות PNG של גרפים.
    """

    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # ----------------------------------------
    # 1) יצירת תיקייה
    # ----------------------------------------
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # ----------------------------------------
    # 2) נתיבי תמונות
    # ----------------------------------------
    img_flags = os.path.join(output_dir, f"{profile_summary['profile_id']}_flags.png")
    img_hit_ratio = os.path.join(output_dir, f"{profile_summary['profile_id']}_hitratio.png")
    img_confusion = os.path.join(output_dir, f"{profile_summary['profile_id']}_cm.png")
    img_predictions = os.path.join(output_dir, f"{profile_summary['profile_id']}_preds.png")

    # ----------------------------------------
    # 3) הפקת הגרפים
    # ----------------------------------------
    df_full = profile_summary["df_full"]  # חייב להכיל date, flag_score, prediction, real, pred_1d, pred_5d

    plot_flags(df_full, save_path=img_flags)
    plot_hit_ratio(df_full, save_path=img_hit_ratio)
    plot_confusion_matrix(df_full, save_path=img_confusion)
    plot_predictions(df_full, save_path=img_predictions)

    # ----------------------------------------
    # 4) בניית HTML
    # ----------------------------------------
    html = TEMPLATE.format(
        profile_id=profile_summary["profile_id"],
        generated_at=generated_at,
        final_flag=profile_summary["flag"],
        confidence=profile_summary["confidence"],
        ml_pred_1d=profile_summary["pred_1d"],
        ml_pred_5d=profile_summary["pred_5d"],
        conflict_resolution=profile_summary["conflict_resolution"],
        conflict_confidence=profile_summary["conflict_confidence"],
        ret_1d=profile_summary["ret_1d"],
        ret_5d=profile_summary["ret_5d"],
        trend_10d=profile_summary["trend_10d"],
        trend_20d=profile_summary["trend_20d"],
        initial_capital=backtest_summary["initial_capital"],
        final_equity=backtest_summary["final_equity"],
        total_return=backtest_summary["total_return"],
        risk_score=risk_score,
        img_flags=img_flags,
        img_hit_ratio=img_hit_ratio,
        img_confusion=img_confusion,
        img_predictions=img_predictions,
    )

    # ----------------------------------------
    # 5) שמירה לקובץ HTML
    # ----------------------------------------
    filename = f"advanced_report_{profile_summary['profile_id']}.html"
    full_path = os.path.join(output_dir, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)

    return full_path
