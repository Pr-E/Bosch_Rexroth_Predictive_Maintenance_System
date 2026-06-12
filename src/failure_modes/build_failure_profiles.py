import joblib
import pandas as pd

from config.constants import (
    S3_BUCKET_NAME,
    FAILURE_PROFILES_PATH
)

from src.logger import (
    configure_logger
)

from src.cloud.s3_storage import (
    S3Storage
)

logging = configure_logger()


# ==========================================================
# FAILURE PROFILE BUILDER
# ==========================================================

class FailureProfileBuilder:

    def __init__(self):

        self.s3 = S3Storage(
            S3_BUCKET_NAME
        )

        self.profile_features = [

            "predicted_rul",

            "pressure_flow_ratio",

            "cumulative_vibration_exposure",

            "thermal_stress_accumulation",

            "equipment_age_days",

            "days_since_filter_change",

            "days_since_last_maintenance",

            "cumulative_downtime_exposure",

            "thermal_hydraulic_stress",

            "rolling_vibration_energy",

            "pressure_bar",

            "flow_lpm",

            "temp_celsius",

            "pump_rpm",

            "vibration_magnitude"
        ]

    # ======================================================
    # LOAD FEATURE STORE
    # ======================================================

    def load_data(self):

        logging.info(
            "Loading feature store from S3..."
        )

        csv_key = self.s3.get_latest_file(

            prefix="feature_store/",

            keyword="rul_dataset"
        )

        self.df = self.s3.load_csv(
            csv_key
        )

        logging.info(

            f"Dataset Loaded: "

            f"{len(self.df):,} rows"
        )

    # ======================================================
    # BUILD FAILURE PROFILES
    # ======================================================

    def build_profiles(self):

        logging.info(
            "Building Failure Profiles..."
        )

        if "failure_mode" not in self.df.columns:

            raise ValueError(
                "failure_mode column missing."
            )

        self.df["predicted_rul"] = (
            self.df["rul_hours"]
        )

        available_features = [

            feature

            for feature

            in self.profile_features

            if feature in self.df.columns
        ]

        self.failure_profiles = {}

        for failure_mode in (

            self.df["failure_mode"]

            .dropna()

            .unique()
        ):

            subset = (

                self.df[

                    self.df[
                        "failure_mode"
                    ]

                    == failure_mode
                ]
            )

            self.failure_profiles[
                failure_mode
            ] = {

                "mean": (

                    subset[
                        available_features
                    ]

                    .mean()

                    .to_dict()
                ),

                "median": (

                    subset[
                        available_features
                    ]

                    .median()

                    .to_dict()
                ),

                "std": (

                    subset[
                        available_features
                    ]

                    .std()

                    .fillna(0)

                    .to_dict()
                ),

                "count": int(
                    len(subset)
                ),

                "features": (
                    available_features
                )
            }

        logging.info(

            f"Profiles Built: "

            f"{len(self.failure_profiles)}"
        )

    # ======================================================
    # SAVE PROFILES
    # ======================================================

    def save_profiles(self):

        joblib.dump(

            self.failure_profiles,

            FAILURE_PROFILES_PATH
        )

        logging.info(

            f"Profiles Saved: "

            f"{FAILURE_PROFILES_PATH}"
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate(self):

        print("\n")
        print("=" * 70)
        print("FAILURE MODE PROFILES")
        print("=" * 70)

        for mode, profile in (

            self.failure_profiles.items()
        ):

            print("\n")

            print(
                f"Failure Mode: {mode}"
            )

            print(
                f"Samples: "
                f"{profile['count']:,}"
            )

            print(
                f"Features: "
                f"{len(profile['features'])}"
            )

    # ======================================================
    # PIPELINE
    # ======================================================

    def run(self):

        self.load_data()

        self.build_profiles()

        self.save_profiles()

        self.validate()

        return self.failure_profiles


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    builder = (
        FailureProfileBuilder()
    )

    builder.run()