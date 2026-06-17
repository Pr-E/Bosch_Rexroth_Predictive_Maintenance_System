import os
import dagshub
import mlflow
from dotenv import load_dotenv
from config.constants import MLFLOW_EXPERIMENT_NAME

load_dotenv(override=True)

# CLOUD BASED MLFLOW SETUP

def setup_mlflow():
    dagshub_token = os.getenv("MLFLOW_TOKEN")
    if not dagshub_token:
        raise EnvironmentError("The Mlflow token cant't be accessed...")
    
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    repo_owner = "ejirogoro27"
    repo_name = "Bosch_Rexroth_Predictive_Maintenance_System" 

    tracking_uri = f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

  