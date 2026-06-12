import sys
import numpy as np

from config.constants import (
    CLEANED_DATA_PATH
)

from src.logger import configure_logger
from src.exception import MyException

from src.data.data_preprocessing import (
    DataPreprocessor
)

logging = configure_logger()


# ==========================================================
# DATA CLEANING
# ==========================================================

class DataCleaning:

    def __init__(self):

        self.preprocessor = (

            DataPreprocessor()
        )

        self.df = (

            self.preprocessor

            .merge_datasets()
        )

    # ======================================================
    # CLEAN DATA
    # ======================================================

    def clean_data(self):

        try:

            logging.info(
                "Starting data cleaning..."
            )

            self.df = self.df
            logging.info(f"Missing Values Before Cleaning:\n{self.df.isnull().sum()}")

            # --------------------------------------------------
            # SORT
            # --------------------------------------------------

            self.df = self.df.sort_values(

                [
                    "machine_id",
                    "timestamp"
                ]
            )

            # --------------------------------------------------
            # SENSOR IMPUTATION
            # --------------------------------------------------

            sensor_cols = [

                "pressure_bar",
                "temp_celsius",
                "flow_lpm",
                "vibration_x_g",
                "vibration_y_g",
                "pump_rpm"
            ]

            self.df[sensor_cols] = (

                self.df

                .groupby(
                    "machine_id"
                )[sensor_cols]

                .transform(

                    lambda group:

                    group

                    .interpolate(
                        method="linear"
                    )

                    .ffill()

                    .bfill()
                )
            )

            # --------------------------------------------------
            # DOWNTIME
            # --------------------------------------------------

            self.df[
                "downtime_hours"
            ] = (

                self.df[
                    "downtime_hours"
                ]

                .fillna(0)
            )

            # --------------------------------------------------
            # REMOVE HEALTHY MACHINE
            # --------------------------------------------------

            self.df = (

                self.df[

                    self.df[
                        "machine_id"
                    ]

                    != "HPU_10"
                ]
            )

            # --------------------------------------------------
            # KEEP FAILURE RECORDS
            # --------------------------------------------------

            self.df = (

                self.df[

                    self.df[
                        "failure_mode"
                    ]

                    .notna()
                ]
            )

            # --------------------------------------------------
            # REMOVE FLAGS
            # --------------------------------------------------

            self.df.drop(

                columns=[

                    "is_anomaly",

                    "is_sensor_dropout"
                ],

                errors="ignore",

                inplace=True
            )

            self.df = (

                self.df

                .reset_index(
                    drop=True
                )
            )

            logging.info(
                "Cleaning completed."
            )

            return self.df

        except Exception as e:

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # VALIDATE
    # ======================================================

    def validate_dataset(self):

        logging.info(
            "Validating cleaned dataset..."
        )

        print("\n")
        print("=" * 70)
        print("CLEANING SUMMARY")
        print("=" * 70)

        print(

            f"\nShape: "

            f"{self.df.shape}"
        )

        print(

            f"\nMissing Values After Cleaning: "

            f"{self.df.isnull().sum().sum()}"
        )

        print(

            "\nFailure Distribution:\n"
        )

        print(

            self.df[
                "failure_mode"
            ]

            .value_counts()
        )

        print(

            "\nMachines:\n"
        )

        print(

            sorted(

                self.df[
                    "machine_id"
                ]

                .unique()
            )
        )

    # ======================================================
    # SAVE
    # ======================================================

    def save_dataset(self):

        try:

            self.df.to_csv(

                CLEANED_DATA_PATH,

                index=False
            )

            logging.info(

                f"Cleaned dataset saved to "

                f"{CLEANED_DATA_PATH}"
            )

        except Exception as e:

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # PIPELINE
    # ======================================================

    def run(self):

        self.df = (

            self.clean_data()
        )

        self.validate_dataset()

        self.save_dataset()

        return self.df


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    cleaner = DataCleaning()

    cleaned_df = cleaner.run()

    print("\n")
    print("=" * 70)
    print("DATA CLEANING COMPLETE")
    print("=" * 70)

    print(cleaned_df.head())