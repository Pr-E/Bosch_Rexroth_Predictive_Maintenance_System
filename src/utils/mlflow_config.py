import os
import dagshub
import mlflow
import boto3
import tempfile

from dotenv import load_dotenv

from config.constants import (
    MLFLOW_EXPERIMENT_NAME,
    DAGSHUB_URL,
    REPO_OWNER,
    REPO_NAME 
)

load_dotenv(override=True)


# # LOCAL MLFLOW SETUP

# def setup_mlflow():
#     token = os.getenv("MLFLOW_TOKEN")
#     if not token:
#         raise EnvironmentError("MLFLOW_TOKEN not found.")

#     os.environ["MLFLOW_TRACKING_USERNAME"] = token
#     os.environ["MLFLOW_TRACKING_PASSWORD"] = token

#     dagshub.init(
#         repo_owner="ejirogoro27",
#         repo_name="Bosch_Rexroth_Predictive_Maintenance_System",
#         mlflow=True
#     )

#     mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

# CLOUD BASED MLFLOW SETUP



def setup_mlflow():
    """
    Initialise MLflow with DagsHub remote tracking.
    Uses MLFLOW_TOKEN for authentication.
    """
    dagshub_token = os.getenv("MLFLOW_TOKEN")
    if not dagshub_token:
        raise EnvironmentError("MLFLOW_TOKEN environment variable is not set")

    # Set credentials
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    # Initialise DagsHub repository
    dagshub.init(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        mlflow=True
    )



    mlflow.set_tracking_uri(f"{DAGSHUB_URL}/{REPO_OWNER}/{REPO_NAME}.mlflow")

    # Set the MLflow experiment
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)