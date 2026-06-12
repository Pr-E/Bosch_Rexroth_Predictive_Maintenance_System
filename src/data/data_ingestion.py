import sys
import logging
import pandas as pd

from config.constants import (

    TELEMETRY_DATA_PATH,
    MAINTENANCE_DATA_PATH,
    FAILURE_LABELS_PATH,
    EQUIPMENT_MASTER_PATH
)

from src.logger import configure_logger
from src.exception import MyException

# ==========================================================
# LOGGING
# ==========================================================

logging = configure_logger()

# ==========================================================
# DATA INGESTION
# ==========================================================

class DataIngestion:

    def __init__(self):

        self.sensor_data = None
        self.maintenance_data = None
        self.failure_data = None
        self.equipment_data = None

    # ======================================================
    # LOAD DATASETS
    # ======================================================

    def load_datasets(self):

        try:

            logging.info(
                "Loading telemetry dataset..."
            )

            self.sensor_data = pd.read_csv(
                TELEMETRY_DATA_PATH,
                low_memory=False
            )

            logging.info(
                "Loading maintenance dataset..."
            )

            self.maintenance_data = pd.read_csv(
                MAINTENANCE_DATA_PATH
            )

            logging.info(
                "Loading failure dataset..."
            )

            self.failure_data = pd.read_csv(
                FAILURE_LABELS_PATH
            )

            logging.info(
                "Loading equipment dataset..."
            )

            self.equipment_data = pd.read_csv(
                EQUIPMENT_MASTER_PATH
            )

            logging.info(
                "All datasets loaded successfully."
            )

            logging.info(
                f"Sensor Rows: {len(self.sensor_data):,}"
            )

            logging.info(
                f"Maintenance Rows: {len(self.maintenance_data):,}"
            )

            logging.info(
                f"Failure Rows: {len(self.failure_data):,}"
            )

            logging.info(
                f"Equipment Rows: {len(self.equipment_data):,}"
            )

            return (

                self.sensor_data,

                self.maintenance_data,

                self.failure_data,

                self.equipment_data
            )

        except Exception as e:

            logging.error(
                f"Error loading datasets: {e}"
            )

            raise MyException(
                e,
                sys
            )
        