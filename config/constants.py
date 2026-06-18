import os

from dotenv import load_dotenv

load_dotenv(override=True)

# ==========================================================
# PROJECT ROOT
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# ==========================================================
# SOURCE DATA
# ==========================================================

INPUT_DATA_PATH = os.path.join(
    BASE_DIR,
    "telemetry_data"
)

SENSOR_TELEMETRY_PATH = f"{INPUT_DATA_PATH}/sensor_telemetry.csv"
MAINTENANCE_LOG_PATH = f"{INPUT_DATA_PATH}/maintenance_log.csv"
FAILURE_LABELS_PATH = f"{INPUT_DATA_PATH}/failure_labels.csv"
EQUIPMENT_MASTER_PATH = f"{INPUT_DATA_PATH}/equipment_master.csv"


# ==========================================================
# DATASETS
# ==========================================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

CLEANED_DATA_DIR = os.path.join(
    DATA_DIR,
    "cleaned"
)

PROCESSED_DATA_DIR = os.path.join(
    DATA_DIR,
    "processed"
)

CLEANED_DATA_PATH = os.path.join(
    CLEANED_DATA_DIR,
    "bosch_rexroth_cleaned.csv"
)

# ==========================================================
# ARTIFACTS
# ==========================================================

ARTIFACTS_DIR = os.path.join(
    BASE_DIR,
    "artifacts"
)

PREPROCESSING_DIR = os.path.join(
    ARTIFACTS_DIR,
    "preprocessing"
)

FEATURE_STORE_DIR = os.path.join(
    ARTIFACTS_DIR,
    "feature_store"
)

FAILURE_MODES_DIR = os.path.join(
    ARTIFACTS_DIR,
    "failure_modes"
)

# ==========================================================
# FEATURE STORE FILES
# ==========================================================

FEATURED_DATA_PATH = os.path.join(
    FEATURE_STORE_DIR,
    "rul_dataset.csv"
)

FEATURE_METADATA_PATH = os.path.join(
    FEATURE_STORE_DIR,
    "features_metadata.json"
)

# ==========================================================
# FAILURE MODE ARTIFACTS
# ==========================================================

FAILURE_PROFILES_PATH = os.path.join(
    FAILURE_MODES_DIR,
    "failure_mode_profiles.pkl"
)

# ==========================================================
# MODELS
# ==========================================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

BEST_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "bosch_rul_model.pkl"
)

# ==========================================================
# REPORTS
# ==========================================================

REPORTS_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

RESULTS_PATH = os.path.join(
    REPORTS_DIR,
    "model_comparison.csv"
)

FEATURE_IMPORTANCE_PATH = os.path.join(
    REPORTS_DIR,
    "feature_importance.csv"
)

# ==========================================================
# LOGGING
# ==========================================================

LOGS_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

# ==========================================================
# PROJECT INFO
# ==========================================================

PROJECT_NAME = (
    "Bosch_Rexroth_Predictive_Maintenance"
)

PROJECT_VERSION = "1.0.0"

# ==========================================================
# MODEL ARTIFACT STORAGE
# ==========================================================

MODEL_ARTIFACT_KEY = (
    "models/bosch_rul_model.pkl"
)


FAILURE_PROFILES_KEY = (
    "failure_modes/failure_mode_profiles.pkl"
)

# ==========================================================
# SAMPLE WEIGHTS
# ==========================================================

CRITICAL_WEIGHT_RUL = 10

HIGH_WEIGHT_RUL = 25

MODERATE_WEIGHT_RUL = 50

LOW_WEIGHT_RUL = 75

# ==========================================================
# MLFLOW
# ==========================================================

MLFLOW_EXPERIMENT_NAME = (
    "bosch_rul_prediction"
)

MODEL_NAME = (
    "bosch_rul_regressor"
)

# ==========================================================
# AWS
# ==========================================================

AWS_REGION = os.getenv(

    "AWS_DEFAULT_REGION",

    "eu-north-1"

).strip()

S3_BUCKET_NAME = (
    "bosch-predictive-maintenance"
)

S3_ARTIFACT_ROOT = (
    f"s3://{S3_BUCKET_NAME}/mlflow-artifacts"
)

FEATURE_DATA_KEY = (
    "feature_store/rul_dataset.csv"
)

FEATURE_METADATA_KEY = (
    "feature_store/features_metadata.json"
)   

# ==========================================================
# AUTO CREATE DIRECTORIES
# ==========================================================

DIRECTORIES = [

    DATA_DIR,

    CLEANED_DATA_DIR,

    PROCESSED_DATA_DIR,

    ARTIFACTS_DIR,

    PREPROCESSING_DIR,

    FEATURE_STORE_DIR,

    FAILURE_MODES_DIR,

    MODEL_DIR,

    REPORTS_DIR,

    LOGS_DIR
]

for directory in DIRECTORIES:

    os.makedirs(
        directory,
        exist_ok=True
    )


