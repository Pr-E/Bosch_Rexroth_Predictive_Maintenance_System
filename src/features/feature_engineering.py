import sys
import json
import io
import os

import numpy as np
import pandas as pd

from config.constants import (
    S3_BUCKET_NAME,
    FEATURE_DATA_KEY,
    FEATURE_METADATA_KEY,
    FEATURE_STORE_DIR,
    FEATURED_DATA_PATH,
    FEATURE_METADATA_PATH
)

from src.logger import configure_logger
from src.exception import MyException

from src.cloud.s3_storage import (
    S3Storage
)

from src.data.data_cleaning import (
    DataCleaning
)

logging = configure_logger()


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

class FeatureEngineering:

    def __init__(self):
        self.cleaner = DataCleaning()
        self.s3 = S3Storage(S3_BUCKET_NAME)
        self.df = None

    # ======================================================
    # FEATURE ENGINEERING
    # ======================================================

    def engineer_features(self):
        try:
            logging.info("Starting feature engineering...")

            self.df = self.cleaner.run()

            # ==================================================
            # SORT DATA
            # ==================================================
            self.df = (
                self.df
                .sort_values(["machine_id", "timestamp"])
                .reset_index(drop=True)
            )

            # ==================================================
            # VIBRATION MAGNITUDE
            # ==================================================
            self.df["vibration_magnitude"] = np.sqrt(
                self.df["vibration_x_g"] ** 2 +
                self.df["vibration_y_g"] ** 2
            )

            # ==================================================
            # MAINTENANCE FEATURES
            # ==================================================
            self.df["days_since_last_maintenance"] = (
                self.df["timestamp"] - self.df["last_maintenance_timestamp"]
            ).dt.total_seconds() / 86400

            # ==================================================
            # EQUIPMENT FEATURES
            # ==================================================
            self.df["equipment_age_days"] = (
                self.df["timestamp"] - self.df["installation_date"]
            ).dt.days

            self.df["days_since_filter_change"] = (
                self.df["timestamp"] - self.df["last_filter_change_date"]
            ).dt.days

            # ==================================================
            # EXPOSURE FEATURES
            # ==================================================
            self.df["cumulative_downtime_exposure"] = (
                self.df
                .groupby("machine_id")["downtime_hours"]
                .cumsum()
            )

            self.df["cumulative_vibration_exposure"] = (
                self.df
                .groupby("machine_id")["vibration_magnitude"]
                .cumsum()
            )

            # ==================================================
            # HYDRAULIC FEATURES
            # ==================================================
            self.df["pressure_flow_ratio"] = (
                self.df["pressure_bar"] / (self.df["flow_lpm"] + 1e-6)
            )

            self.df["thermal_hydraulic_stress"] = (
                self.df["temp_celsius"] *
                self.df["pressure_bar"] /
                (self.df["flow_lpm"] + 1)
            )

            self.df["thermal_stress_accumulation"] = (
                self.df
                .groupby("machine_id")["thermal_hydraulic_stress"]
                .cumsum()
            )

            # ======================================================
            # LAG FEATURES
            # ======================================================
            lag3_features = [
                "vibration_magnitude",
                "pressure_bar",
                "temp_celsius"
            ]

            for col in lag3_features:
                feature_name = f"{col}_lag_3"
                self.df[feature_name] = (
                    self.df
                    .groupby("machine_id")[col]
                    .shift(3)
                )

            lag6_features = [
                "pressure_bar",
                "flow_lpm",
                "pump_rpm",
                "temp_celsius"
            ]

            for col in lag6_features:
                feature_name = f"{col}_lag_6"
                self.df[feature_name] = (
                    self.df
                    .groupby("machine_id")[col]
                    .shift(6)
                )

            # ==================================================
            # DELTA FEATURES
            # ==================================================
            delta_cols = [
                "pressure_bar",
                "temp_celsius",
                "flow_lpm",
                "vibration_magnitude"
            ]

            for col in delta_cols:
                feature_name = f"{col}_delta_1"
                self.df[feature_name] = (
                    self.df
                    .groupby("machine_id")[col]
                    .diff()
                )

            # ==================================================
            # ACCELERATION FEATURES
            # ==================================================
            delta_cols = [
                "pressure_bar",
                "temp_celsius",
                "flow_lpm",
                "vibration_magnitude"
            ]

            for col in delta_cols:
                feature_name = f"{col}_acceleration"
                self.df[feature_name] = (
                    self.df
                    .groupby("machine_id")[f"{col}_delta_1"]
                    .diff()
                )

            # ==================================================
            # ROLLING FEATURES
            # ==================================================
            rolling_cols = [
                "vibration_magnitude",
                "flow_lpm",
                "pump_rpm"
            ]

            for col in rolling_cols:
                self.df[f"{col}_rolling_std_6"] = (
                    self.df
                    .groupby("machine_id")[col]
                    .transform(
                        lambda x: x.rolling(window=6, min_periods=1).std()
                    )
                )

            self.df["rolling_vibration_energy"] = (
                self.df["vibration_magnitude"] ** 2
            )

            self.df["rolling_vibration_energy"] = (
                self.df
                .groupby("machine_id")["rolling_vibration_energy"]
                .transform(
                    lambda x: x.rolling(window=6, min_periods=1).mean()
                )
            )

            # ==================================================
            # TREND FEATURES
            # ==================================================
            trend_cols = [
                "vibration_magnitude",
                "pressure_bar",
                "temp_celsius"
            ]

            for col in trend_cols:
                self.df[f"{col}_trend_slope_15"] = (
                    self.df
                    .groupby("machine_id")[col]
                    .transform(lambda x: x.diff(15))
                )

            # ==================================================
            # DROP REDUNDANT COLUMNS
            # ==================================================
            self.df.drop(
                columns=[
                    "shift",
                    "vibration_x_g",
                    "vibration_y_g",
                    "installation_date",
                    "last_filter_change_date",
                    "last_maintenance_timestamp"
                ],
                errors="ignore",
                inplace=True
            )

            # ==================================================
            # FEATURE GROUPS
            # ==================================================
            SENSOR_COLS = [
                "pressure_bar",
                "temp_celsius",
                "flow_lpm",
                "pump_rpm",
                "vibration_magnitude"
            ]

            NON_TEMPORAL_FEATURES = [
                "days_since_last_maintenance",
                "equipment_age_days",
                "days_since_filter_change",
                "cumulative_downtime_exposure",
                "cumulative_vibration_exposure",
                "pressure_flow_ratio",
                "thermal_hydraulic_stress",
                "thermal_stress_accumulation"
            ]

            TEMPORAL_FEATURES = [
                col for col in self.df.columns
                if ("lag" in col or "rolling" in col or "trend" in col or "delta" in col or "acceleration" in col)
            ]

            BASE_FEATURES_RUL = SENSOR_COLS + NON_TEMPORAL_FEATURES

            FINAL_FEATURES_RUL = [
                feature for feature in (BASE_FEATURES_RUL + TEMPORAL_FEATURES)
                if feature in self.df.columns
            ]

            # ==================================================
            # REMOVE NULLS
            # ==================================================
            self.df = (
                self.df
                .dropna()
                .reset_index(drop=True)
            )

            # ==================================================
            # FINAL DATASET
            # ==================================================
            rul_dataset = self.df[
                FINAL_FEATURES_RUL +
                [
                    "failure_mode",
                    "rul_hours",
                    "machine_id",
                    "timestamp"
                ]
            ]

            feature_store = {
                "SENSOR_COLS": SENSOR_COLS,
                "FINAL_FEATURES_RUL": FINAL_FEATURES_RUL
            }

            return (rul_dataset, feature_store)

        except Exception as e:
            raise MyException(e, sys)

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate_features(self, rul_dataset, feature_store):
        logging.info("Validating engineered dataset...")

        print("\n" + "=" * 80)
        print("FEATURE ENGINEERING SUMMARY")
        print("=" * 80)

        print(f"\nDataset Shape: {rul_dataset.shape}")
        print(f"\nFinal Features: {len(feature_store['FINAL_FEATURES_RUL'])}")
        print(f"\nMissing Values: {rul_dataset.isnull().sum().sum()}")

        print("\nRUL Distribution:\n")
        print(rul_dataset["rul_hours"].describe().round(2))

    # ======================================================
    # UPLOAD TO S3
    # ======================================================

    def upload_feature_store(self, rul_dataset, feature_store):
        csv_buffer = io.StringIO()
        rul_dataset.to_csv(csv_buffer, index=False)

        self.s3.upload_bytes(
            data=csv_buffer.getvalue(),
            s3_key=FEATURE_DATA_KEY,
            content_type="text/csv"
        )

        self.s3.upload_bytes(
            data=json.dumps(feature_store, indent=4),
            s3_key=FEATURE_METADATA_KEY,
            content_type="application/json"
        )

        logging.info("Feature Store uploaded to S3.")

        # ======================================================
        # SAVE LOCAL COPY
        # ======================================================
        os.makedirs(FEATURE_STORE_DIR, exist_ok=True)

        rul_dataset.to_csv(FEATURED_DATA_PATH, index=False)

        with open(FEATURE_METADATA_PATH, "w") as f:
            json.dump(feature_store, f, indent=4)

        logging.info(f"Local feature dataset saved: {FEATURED_DATA_PATH}")
        logging.info(f"Local metadata saved: {FEATURE_METADATA_PATH}")

    # ======================================================
    # PIPELINE
    # ======================================================

    def run(self):
        rul_dataset, feature_store = self.engineer_features()

        self.validate_features(rul_dataset, feature_store)
        self.upload_feature_store(rul_dataset, feature_store)

        return (rul_dataset, feature_store["FINAL_FEATURES_RUL"])


features = FeatureEngineering()
features.engineer_features()