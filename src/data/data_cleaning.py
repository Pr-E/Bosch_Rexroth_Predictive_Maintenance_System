import sys
import numpy as np

from config.constants import CLEANED_DATA_PATH
from src.logger import configure_logger
from src.exception import MyException
from src.data.data_preprocessing import DataPreprocessor

logging = configure_logger()


class DataCleaning:

    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.df = self.preprocessor.merge_datasets()

    def clean_data(self):
        try:
            logging.info("Starting data cleaning...")

            self.df = self.df
            logging.info(f"Missing Values Before Cleaning:\n{self.df.isnull().sum()}")

            # Sort by machine and timestamp
            self.df = self.df.sort_values(["machine_id", "timestamp"])

            # Interpolate sensor columns per machine
            sensor_cols = [
                "pressure_bar", "temp_celsius", "flow_lpm",
                "vibration_x_g", "vibration_y_g", "pump_rpm"
            ]
            self.df[sensor_cols] = (
                self.df
                .groupby("machine_id")[sensor_cols]
                .transform(lambda group: group.interpolate(method="linear").ffill().bfill())
            )

            # Fill downtime
            self.df["downtime_hours"] = self.df["downtime_hours"].fillna(0)

            # Remove healthy machine HPU_10
            self.df = self.df[self.df["machine_id"] != "HPU_10"]

            # Keep only records with a failure mode
            self.df = self.df[self.df["failure_mode"].notna()]

            # Drop flag columns
            self.df.drop(columns=["is_anomaly", "is_sensor_dropout"], errors="ignore", inplace=True)

            self.df = self.df.reset_index(drop=True)

            logging.info("Cleaning completed.")
            return self.df

        except Exception as e:
            raise MyException(e, sys)

    def validate_dataset(self):
        logging.info("Validating cleaned dataset...")

        print("\n" + "=" * 70)
        print("CLEANING SUMMARY")
        print("=" * 70)

        print(f"\nShape: {self.df.shape}")
        print(f"\nMissing Values After Cleaning: {self.df.isnull().sum().sum()}")
        print("\nFailure Distribution:\n")
        print(self.df["failure_mode"].value_counts())
        print("\nMachines:\n")
        print(sorted(self.df["machine_id"].unique()))

    def save_dataset(self):
        try:
            self.df.to_csv(CLEANED_DATA_PATH, index=False)
            logging.info(f"Cleaned dataset saved to {CLEANED_DATA_PATH}")
        except Exception as e:
            raise MyException(e, sys)

    def run(self):
        self.df = self.clean_data()
        self.validate_dataset()
        self.save_dataset()
        return self.df


# if __name__ == "__main__":
#     cleaner = DataCleaning()
#     cleaned_df = cleaner.run()

#     print("\n" + "=" * 70)
#     print("DATA CLEANING COMPLETE")
#     print("=" * 70)
#     print(cleaned_df.head())