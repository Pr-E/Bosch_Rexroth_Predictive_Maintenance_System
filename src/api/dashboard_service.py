"""
Service to compute executive dashboard KPIs from the actual
feature store and the latest model summary stored on S3.
"""

import pandas as pd
from config.constants import S3_BUCKET_NAME
from src.cloud.s3_storage import S3Storage
from src.logger import configure_logger

logging = configure_logger()

class DashboardKPIService:
    def __init__(self):
        self.s3 = S3Storage(S3_BUCKET_NAME)

    def _load_feature_store(self) -> pd.DataFrame:
        """Load the latest feature store CSV from S3."""
        csv_key = self.s3.get_latest_file(
            prefix="feature_store/",
            keyword="rul_dataset"
        )
        df = self.s3.load_csv(csv_key)
        logging.info("Feature store loaded: %d rows, %d columns", df.shape[0], df.shape[1])
        return df

    def _load_model_summary(self) -> dict:
        """Load the model summary JSON saved during training."""
        summary_key = "model-registry/latest_model_summary.json"
        return self.s3.load_json(summary_key)

    def get_kpis(self) -> dict:
        # Load feature store
        df = self._load_feature_store()

        # Fleet KPIs
        degraded_machines = df["machine_id"].nunique()
        telemetry_records = len(df)
        # Engineered features: count of columns that are not IDs/labels
        # Assuming columns: machine_id, timestamp, failure_mode, rul_hours are non-features
        feature_cols = [c for c in df.columns
                        if c not in ["machine_id", "timestamp", "failure_mode", "rul_hours"]]
        engineered_features = len(feature_cols)
        avg_rul_hours = float(df["rul_hours"].mean())

        # Failure distribution
        failure_dist = df["failure_mode"].value_counts().reset_index()
        failure_dist.columns = ["failure_mode", "count"]
        failure_dist = failure_dist.to_dict(orient="records")

        # Model info from summary
        try:
            summary = self._load_model_summary()
            r2 = summary["r2_score"]
            mae = summary["mae_hours"]
            model_version = summary["model_version"]
            training_date = summary["training_date"]
            feature_importance = summary["feature_importance"]
        except Exception as e:
            logging.error("Could not load model summary: %s", e)
            # In production you might want to raise an error,
            # but for robustness we set placeholders.
            r2 = 0.0
            mae = 0.0
            model_version = "unknown"
            training_date = "unknown"
            feature_importance = []

        return {
            "degraded_machines": int(degraded_machines),
            "telemetry_records": int(telemetry_records),
            "engineered_features": int(engineered_features),
            "avg_rul_hours": round(avg_rul_hours, 2),
            "r2_score": round(r2, 4),
            "mae_hours": round(mae, 2),
            "feature_importance": feature_importance,
            "failure_distribution": failure_dist,
            "model_version": model_version,
            "training_date": training_date
        }