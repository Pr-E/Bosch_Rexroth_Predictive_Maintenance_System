import os
import tempfile
import joblib

import mlflow
import mlflow.sklearn

from config.constants import MODEL_NAME, S3_BUCKET_NAME
from src.logger import configure_logger
from src.cloud.s3_storage import S3Storage
from src.utils.mlflow_config import setup_mlflow

logging = configure_logger()


class ModelRegistry:

    def __init__(self):
        self.bucket_name = S3_BUCKET_NAME
        self.model_name = MODEL_NAME
        setup_mlflow()
        self.s3 = S3Storage(bucket_name=self.bucket_name)

    def register(self, model, params: dict, metrics: dict, tags: dict = None) -> dict:
        tags = tags or {}

        with mlflow.start_run(tags={"model_name": self.model_name, **tags}) as run:
            run_id = run.info.run_id

            # Log parameters
            mlflow.log_params(params)
            logging.info("Parameters logged to MLflow.")

            # Log metrics
            mlflow.log_metrics({
                "rmse": metrics["rmse"],
                "mae": metrics["mae"],
                "r2": metrics["r2"]
            })
            logging.info(f"RMSE={metrics['rmse']:.4f} | MAE={metrics['mae']:.4f} | R2={metrics['r2']:.4f}")

            # Register model
            mlflow.sklearn.log_model(
                sk_model=model,
                name="model",
                registered_model_name=self.model_name
            )
            logging.info(f"Model registered: {self.model_name}")

            # S3 backup
            with tempfile.TemporaryDirectory() as tmpdir:
                local_model_path = os.path.join(tmpdir, f"{self.model_name}.joblib")
                joblib.dump(model, local_model_path)
                s3_uri = self.s3.upload_model(
                    local_path=local_model_path,
                    model_name=self.model_name,
                    run_id=run_id
                )

        summary = {
            "run_id": run_id,
            "model_name": self.model_name,
            "s3_uri": s3_uri,
            "metrics": metrics
        }

        logging.info("Model registration completed.")
        return summary