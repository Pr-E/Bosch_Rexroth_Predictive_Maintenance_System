import os
import dagshub
import mlflow
from dotenv import load_dotenv
from config.constants import MLFLOW_EXPERIMENT_NAME

load_dotenv(override=True)

# ------------------------------------------------------------------
# MLflow Configuration (DagsHub)
# ------------------------------------------------------------------
def setup_mlflow():
    token = os.getenv("MLFLOW_TOKEN")
    if not token:
        raise EnvironmentError("MLFLOW_TOKEN not found.")

    os.environ["MLFLOW_TRACKING_USERNAME"] = token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token

    dagshub.init(
        repo_owner="ejirogoro27",
        repo_name="Bosch_Rexroth_Predictive_Maintenance_System",
        mlflow=True
    )

    mlflow.set_tracking_uri(
        "https://dagshub.com/ejirogoro27/Bosch_Rexroth_Predictive_Maintenance_System.mlflow"
    )

    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)