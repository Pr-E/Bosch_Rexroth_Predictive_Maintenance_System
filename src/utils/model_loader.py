import json
import joblib
import mlflow

from mlflow.tracking import MlflowClient

from config.constants import MODEL_NAME, FEATURE_METADATA_PATH
from src.utils.mlflow_config import setup_mlflow


def load_prediction_objects():
    setup_mlflow()

    client = MlflowClient()
    versions = client.get_latest_versions(MODEL_NAME)

    if len(versions) == 0:
        raise ValueError("No registered model found.")

    latest = max(versions, key=lambda x: int(x.version))
    model_uri = f"models:/{MODEL_NAME}/{latest.version}"
    model = mlflow.sklearn.load_model(model_uri)

    with open(FEATURE_METADATA_PATH, "r") as file:
        features = json.load(file)

    return {"model": model, "features": features}