import os
import sys
import joblib
import json
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from config.constants import (
    MODEL_NAME,
    S3_BUCKET_NAME,
    CRITICAL_WEIGHT_RUL,
    HIGH_WEIGHT_RUL,
    MODERATE_WEIGHT_RUL,
    LOW_WEIGHT_RUL,
    FEATURE_IMPORTANCE_PATH,
    REPORTS_DIR
)

from src.logger import configure_logger
from src.exception import MyException
from src.cloud.s3_storage import S3Storage
from src.features.feature_engineering import FeatureEngineering
from lightgbm import LGBMRegressor
from src.utils.model_registry import ModelRegistry

logging = configure_logger()


class ModellingPipeline:

    def __init__(self):
        self.s3 = S3Storage(S3_BUCKET_NAME)
        self.rul_data = None
        self.feature_sets = None
        self.FINAL_FEATURES_RUL = None
        self.model = None

    def run_feature_engineering(self):
        try:
            logging.info("Running Feature Engineering...")
            FeatureEngineering().run()
            logging.info("Feature Engineering Complete.")
        except Exception as e:
            raise MyException(e, sys)

    def load_data(self):
        try:
            logging.info("Loading Feature Store...")
            csv_key = self.s3.get_latest_file(prefix="feature_store/", keyword="rul_dataset")
            json_key = self.s3.get_latest_file(prefix="feature_store/", keyword="features_metadata")

            self.rul_data = self.s3.load_csv(csv_key)
            self.feature_sets = self.s3.load_json(json_key)
            self.FINAL_FEATURES_RUL = self.feature_sets["FINAL_FEATURES_RUL"]

            logging.info(f"Rows Loaded: {len(self.rul_data):,}")
            logging.info(f"Features Loaded: {len(self.FINAL_FEATURES_RUL)}")
        except Exception as e:
            raise MyException(e, sys)

    def prepare_data(self):
        try:
            logging.info("Preparing Model Data...")

            self.rul_data = self.rul_data.sort_values("timestamp").reset_index(drop=True)

            split_time = self.rul_data["timestamp"].quantile(0.80)
            self.train_end_time = split_time
            self.test_start_time = self.rul_data[self.rul_data["timestamp"] > split_time]["timestamp"].min()

            train = self.rul_data[self.rul_data["timestamp"] <= split_time]
            test = self.rul_data[self.rul_data["timestamp"] > split_time]

            self.X_train = train[self.FINAL_FEATURES_RUL]
            self.y_train = train["rul_hours"]
            self.X_test = test[self.FINAL_FEATURES_RUL]
            self.y_test = test["rul_hours"]

            # Sample weights
            self.sample_weights = np.where(
                self.y_train <= CRITICAL_WEIGHT_RUL, 6.0,
                np.where(self.y_train <= HIGH_WEIGHT_RUL, 4.0,
                         np.where(self.y_train <= MODERATE_WEIGHT_RUL, 3.0,
                                  np.where(self.y_train <= LOW_WEIGHT_RUL, 2.0, 1.5)))
            )

            # Validation prints
            print("\n" + "=" * 70)
            print("RUL REGRESSION DATA PREPARATION")
            print("=" * 70)
            print(f"\nRegression Features: {len(self.FINAL_FEATURES_RUL)}")
            print(f"\nTraining End: {self.train_end_time}")
            print(f"Testing Start: {self.test_start_time}")
            print("\nTrain RUL Distribution")
            print(self.y_train.describe().round(2))
            print("\nTest RUL Distribution")
            print(self.y_test.describe().round(2))
            print(f"\nRUL < 75 Hours:\n{(self.y_train < 75).sum():,}")
            print(f"\nRUL < 50 Hours:\n{(self.y_train < 50).sum():,}")
            print(f"\nRUL < 25 Hours:\n{(self.y_train < 25).sum():,}")
            print(f"\nRUL < 10 Hours:\n{(self.y_train < 10).sum():,}")
            print(f"\nTrain Shape:\n{self.X_train.shape}")
            print(f"\nTest Shape:\n{self.X_test.shape}")
            print("\n✓ Temporal split complete")
        except Exception as e:
            raise MyException(e, sys)

    def train_model(self):
        logging.info("Training LightGBM Model...")
        self.model = LGBMRegressor(
            objective="regression",
            n_estimators=500,
            max_depth=8,
            learning_rate=0.03,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=-1
        )
        self.model.fit(self.X_train, self.y_train, sample_weight=self.sample_weights)
        logging.info("Model Training Complete")

    def executive_feature_mapper(self, feature):
        feature = feature.lower()
        if "vibration" in feature:
            return "Vibration Health"
        elif "thermal" in feature:
            return "Thermal Stress"
        elif "pressure" in feature:
            return "Hydraulic Pressure"
        elif "flow" in feature:
            return "Hydraulic Flow"
        elif "maintenance" in feature:
            return "Maintenance History"
        elif "downtime" in feature:
            return "Downtime Exposure"
        elif "filter" in feature:
            return "Filter Health"
        elif "equipment_age" in feature:
            return "Asset Age"
        elif "rpm" in feature:
            return "Pump Performance"
        else:
            return "Other Factors"

    def evaluate(self):
        predictions = self.model.predict(self.X_test)

        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        importance = pd.DataFrame({
            "feature": self.FINAL_FEATURES_RUL,
            "importance": self.model.feature_importances_
        }).sort_values("importance", ascending=False)

        importance.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

        # Technical plot
        self.technical_png = os.path.join(REPORTS_DIR, "feature_importance.png")
        plt.figure(figsize=(10, 8))
        top20 = importance.head(20)
        plt.barh(top20["feature"], top20["importance"])
        plt.tight_layout()
        plt.savefig(self.technical_png)
        plt.close()

        # Executive grouped importance
        executive = importance.copy()
        executive["category"] = executive["feature"].apply(self.executive_feature_mapper)
        executive = executive.groupby("category")["importance"].sum().reset_index().sort_values("importance", ascending=False)

        self.executive_csv = os.path.join(REPORTS_DIR, "executive_feature_importance.csv")
        executive.to_csv(self.executive_csv, index=False)

        self.executive_png = os.path.join(REPORTS_DIR, "executive_feature_importance.png")
        plt.figure(figsize=(8, 6))
        plt.barh(executive["category"], executive["importance"])
        plt.tight_layout()
        plt.savefig(self.executive_png)
        plt.close()

        # Store DataFrames for later use (e.g., saving summary)
        self.importance_df = importance
        self.executive_importance_df = executive

        print("\n" + "=" * 80)
        print("LIGHTGBM RESULTS")
        print("=" * 80)
        print(f"\nMAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R²: {r2:.4f}")
        print("\nTop Features:\n")
        print(importance.head(20))

        return mae, rmse, r2

    def save_model_summary(self, mae, rmse, r2):
        """
        Upload a live summary of the latest training run to S3.
        Uses executive feature importance for business readability.
        """
        # Prefer executive mapping; fallback to raw top‑10
        if hasattr(self, 'executive_importance_df') and not self.executive_importance_df.empty:
            importance_list = self.executive_importance_df.to_dict(orient="records")
        else:
            top10 = self.importance_df.head(10)
            importance_list = [
                {"feature": row["feature"], "importance": row["importance"]}
                for _, row in top10.iterrows()
            ]

        summary = {
            "model_version": datetime.now().strftime("%Y%m%d%H%M%S"),
            "training_date": datetime.now().isoformat(),
            "r2_score": round(float(r2), 4),
            "mae_hours": round(float(mae), 2),
            "rmse_hours": round(float(rmse), 2),
            "features_count": len(self.FINAL_FEATURES_RUL),
            "feature_importance": importance_list
        }

        self.s3.upload_json(summary, "model-registry/latest_model_summary.json")
        logging.info("Model summary uploaded to S3.")

    def run(self):
        self.run_feature_engineering()
        self.load_data()
        self.prepare_data()
        self.train_model()
        mae, rmse, r2 = self.evaluate()

        # Save live dashboard summary (executive‑style)
        try:
            self.save_model_summary(mae, rmse, r2)
        except Exception as e:
            logging.warning(f"Could not save model summary: {e}")

        # Register model
        try:
            registry = ModelRegistry()
            registry.register(
                model=self.model,
                params=self.model.get_params(),
                metrics={"mae": mae, "rmse": rmse, "r2": r2},
                tags={"stage": "dev", "dataset": "hydraulic_system"}
            )
            logging.info("Modelling Pipeline Completed.")
        except Exception as e:
            logging.warning(f"Registry skipped: {e}")

        return self.model