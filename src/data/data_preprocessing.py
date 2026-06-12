import sys
import pandas as pd

from src.logger import configure_logger
from src.exception import MyException

from src.data.data_ingestion import (
    DataIngestion
)

logging = configure_logger()


# ==========================================================
# DATA PREPROCESSOR
# ==========================================================

class DataPreprocessor:

    def __init__(self):
        ingestion = DataIngestion()

        (
            self.sensor_data,
            self.maintenance_data,
            self.failure_data,
            self.equipment_data
        ) = ingestion.load_datasets()

    # ======================================================
    # DATA MERGING
    # ======================================================

    def merge_datasets(self):
        try:
            logging.info("Starting data preprocessing...")

            # --------------------------------------------------
            # TIMESTAMP CONVERSION
            # --------------------------------------------------
            logging.info("Converting timestamps...")

            self.sensor_data["timestamp"] = pd.to_datetime(
                self.sensor_data["timestamp"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            )

            self.maintenance_data["action_timestamp"] = pd.to_datetime(
                self.maintenance_data["action_timestamp"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            )

            self.equipment_data["installation_date"] = pd.to_datetime(
                self.equipment_data["installation_date"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            )

            self.equipment_data["last_filter_change_date"] = pd.to_datetime(
                self.equipment_data["last_filter_change_date"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            )

            # --------------------------------------------------
            # REMOVE INVALID TIMESTAMPS
            # --------------------------------------------------
            sensor_df = (
                self.sensor_data
                .dropna(subset=["timestamp"])
                .copy()
            )

            maintenance_df = (
                self.maintenance_data
                .dropna(subset=["action_timestamp"])
                .copy()
            )

            # --------------------------------------------------
            # SORT DATA
            # --------------------------------------------------
            sensor_df = sensor_df.sort_values(["machine_id", "timestamp"])
            maintenance_df = maintenance_df.sort_values(["machine_id", "action_timestamp"])

            # --------------------------------------------------
            # UNIX TIMESTAMP
            # --------------------------------------------------
            sensor_df["ts_num"] = (
                sensor_df["timestamp"].astype("int64") // 10**9
            )

            maintenance_df["maint_ts"] = (
                maintenance_df["action_timestamp"].astype("int64") // 10**9
            )

            # --------------------------------------------------
            # MAINTENANCE MERGE
            # --------------------------------------------------
            merged_df = pd.merge_asof(
                sensor_df.sort_values("ts_num"),
                maintenance_df[
                    ["machine_id", "maint_ts", "action_timestamp"]
                ].sort_values("maint_ts"),
                left_on="ts_num",
                right_on="maint_ts",
                by="machine_id",
                direction="backward"
            )

            merged_df.rename(
                columns={"action_timestamp": "last_maintenance_timestamp"},
                inplace=True
            )

            # --------------------------------------------------
            # FAILURE MERGE
            # --------------------------------------------------
            merged_df = merged_df.merge(
                self.failure_data[["machine_id", "downtime_hours"]],
                on="machine_id",
                how="left"
            )

            # --------------------------------------------------
            # EQUIPMENT MERGE
            # --------------------------------------------------
            merged_df = merged_df.merge(
                self.equipment_data[[
                    "machine_id",
                    "installation_date",
                    "last_filter_change_date"
                ]],
                on="machine_id",
                how="left"
            )

            # --------------------------------------------------
            # DROP TEMP COLUMNS
            # --------------------------------------------------
            merged_df.drop(
                columns=["ts_num", "maint_ts"],
                errors="ignore",
                inplace=True
            )

            merged_df = (
                merged_df
                .sort_values(["machine_id", "timestamp"])
                .reset_index(drop=True)
            )

            logging.info(f"Preprocessed Shape: {merged_df.shape}")

            return merged_df

        except Exception as e:
            raise MyException(e, sys)


# ==========================================================
# TEST
# ==========================================================

# if __name__ == "__main__":
#     processor = DataPreprocessor()
#     df = processor.merge_datasets()
# 
#     print("\n")
#     print("=" * 70)
#     print("PREPROCESSING COMPLETE")
#     print("=" * 70)
# 
#     print(df.head())
# 
#     print("\nShape:")
#     print(df.shape)