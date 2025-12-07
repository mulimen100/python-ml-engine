import pandas as pd
from ..ingestion.load_snapshot import load_snapshot
from ..compute.compute_returns import compute_returns
from ..compute.compute_trends import compute_trends
from ..ml.feature_matrix import build_feature_matrix
from ..ml.predict import load_models, make_predictions
from ..compute.final_flag_v2 import compute_flag_v2
from ..compute.conflict_resolver import resolve_conflict

class ProfileEngine:
    """
    מנוע מלא לפרופיל אחד (Multi-Profile)
    """

    def __init__(self, profile_id, df_source):
        self.profile_id = profile_id
        self.df = df_source[df_source["profile_id"] == profile_id].reset_index(drop=True)

    def compute_all(self):
        # בסיס
        self.df = compute_returns(self.df)
        self.df = compute_trends(self.df)

        # פיצ'רים מתקדמים (Feature Matrix 2.0)
        features = build_feature_matrix(self.df)

        # טעינת מודלים
        model_daily, model_weekly = load_models()

        # חיזוי
        pred_1d, pred_5d = make_predictions(model_daily, model_weekly, features.tail(1))

        # Flags 2.0
        row = self.df.tail(1).iloc[0]
        flag, score = compute_flag_v2(
            pred_1d,
            pred_5d,
            row["trend_10d"],
            row["trend_20d"],
            row["ret_1d"]
        )

        # Conflict Resolver
        decision, conflict_conf = resolve_conflict(
            pred_1d,
            pred_5d,
            row["trend_20d"],
            score,
            score
        )

        return {
            "profile_id": self.profile_id,
            "pred_1d": pred_1d,
            "pred_5d": pred_5d,
            "flag": flag,
            "confidence": score,
            "conflict_resolution": decision,
            "conflict_confidence": conflict_conf
        }
