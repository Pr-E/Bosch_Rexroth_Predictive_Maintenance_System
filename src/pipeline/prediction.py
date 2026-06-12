import joblib
import numpy as np
import pandas as pd

from config.constants import (
    FAILURE_PROFILES_PATH,
    S3_BUCKET_NAME
)

from src.explainability.executive_narratives import (
    generate_pattern_interpretation
)

from src.utils.model_loader import (
    load_prediction_objects
)

from src.explainability.shap_explainer import (
    ShapExplainer
)

from src.explainability.local_explanations import (
    build_local_explanation
)

from src.explainability.executive_narratives import (
    generate_narrative
)

from src.failure_modes.failure_probability_engine import (
    FailureProbabilityEngine
)

from src.failure_modes.recommendations import (
    generate_recommendations
)

from src.explainability.executive_narratives import (
    generate_narrative,
    generate_pattern_interpretation
)

from src.cloud.s3_storage import S3Storage

from src.logger import (
    configure_logger
)


logging = configure_logger()


# ==========================================================
# PREDICTION SERVICE
# ==========================================================

class PredictionService:

    # ==========================================================
    # INITIALIZE PREDICTION SERVICE
    # ==========================================================

    def __init__(self):
        logging.info("Loading prediction artifacts...")

        # ------------------------------------------------------
        # MODEL OBJECTS
        # ------------------------------------------------------
        objects = load_prediction_objects()

        self.model = objects["model"]
        self.feature_metadata = objects["features"]

        # ------------------------------------------------------
        # FEATURE DEFINITIONS
        # ------------------------------------------------------
        self.feature_cols = self.feature_metadata["FINAL_FEATURES_RUL"]
        self.sensor_cols = self.feature_metadata["SENSOR_COLS"]

        # ------------------------------------------------------
        # LOAD FEATURE STORE
        # ------------------------------------------------------
        self.s3 = S3Storage(S3_BUCKET_NAME)

        csv_key = self.s3.get_latest_file(
            prefix="feature_store/",
            keyword="rul_dataset"
        )

        self.dataset = self.s3.load_csv(csv_key)
        self.dataset["timestamp"] = pd.to_datetime(self.dataset["timestamp"])

        logging.info(f"Feature Store Loaded | Rows: {len(self.dataset):,}")

        # ------------------------------------------------------
        # FAILURE MODE PROFILES
        # ------------------------------------------------------
        self.failure_profiles = joblib.load(FAILURE_PROFILES_PATH)
        logging.info("Failure profiles loaded.")

        # ------------------------------------------------------
        # SHAP EXPLAINABILITY
        # ------------------------------------------------------
        self.shap_explainer = ShapExplainer(self.model)

        # ------------------------------------------------------
        # FAILURE PROBABILITY ENGINE
        # ------------------------------------------------------
        self.failure_engine = FailureProbabilityEngine()

        logging.info("Prediction Service Ready.")


    # ======================================================
    # FEATURE REBUILD
    # ======================================================

    def rebuild_features(self, machine_df, sensor_input):
        latest = machine_df.sort_values("timestamp").iloc[-1]

        new_row = {
            "machine_id": latest["machine_id"],
            "timestamp": pd.Timestamp.now(),
            "pressure_bar": sensor_input["pressure_bar"],
            "temp_celsius": sensor_input["temp_celsius"],
            "flow_lpm": sensor_input["flow_lpm"],
            "pump_rpm": sensor_input["pump_rpm"],
            "vibration_x_g": sensor_input["vibration_x_g"],
            "vibration_y_g": sensor_input["vibration_y_g"]
        }

        # --------------------------------------------------
        # VIBRATION MAGNITUDE
        # --------------------------------------------------
        new_row["vibration_magnitude"] = np.sqrt(
            sensor_input["vibration_x_g"] ** 2 +
            sensor_input["vibration_y_g"] ** 2
        )

        # --------------------------------------------------
        # HISTORICAL FEATURES
        # --------------------------------------------------
        new_row["days_since_last_maintenance"] = latest["days_since_last_maintenance"]
        new_row["equipment_age_days"] = latest["equipment_age_days"]
        new_row["days_since_filter_change"] = latest["days_since_filter_change"]
        new_row["cumulative_downtime_exposure"] = latest["cumulative_downtime_exposure"]

        # REDERIVE THE CUMULATIVE

        # --------------------------------------------------
        # CUMULATIVE VIBRATION EXPOSURE
        # --------------------------------------------------
        new_row["cumulative_vibration_exposure"] = (
            latest["cumulative_vibration_exposure"] +
            new_row["vibration_magnitude"]
        )

        # --------------------------------------------------
        # PRESSURE FLOW RATIO
        # --------------------------------------------------
        new_row["pressure_flow_ratio"] = (
            new_row["pressure_bar"] / max(new_row["flow_lpm"], 1)
        )

        # --------------------------------------------------
        # THERMAL STRESS
        # --------------------------------------------------
        previous_thermal = latest["thermal_stress_accumulation"]
        current_stress = new_row["temp_celsius"] * new_row["pressure_bar"]
        new_row["thermal_stress_accumulation"] = previous_thermal + current_stress

        # --------------------------------------------------
        # THERMAL HYDRAULIC STRESS
        # --------------------------------------------------
        new_row["thermal_hydraulic_stress"] = (
            new_row["temp_celsius"] * new_row["pressure_flow_ratio"]
        )

        history = machine_df.sort_values("timestamp").tail(15)

        combined = pd.concat(
            [history, pd.DataFrame([new_row])],
            ignore_index=True
        ).sort_values("timestamp").reset_index(drop=True)

        return combined

    # ======================================================
    # LAGS
    # ======================================================

    def create_lag_features(self, combined):
        lag_map = {
            "vibration_magnitude": [3],
            "pressure_bar": [3, 6],
            "temp_celsius": [3, 6],
            "flow_lpm": [6],
            "pump_rpm": [6]
        }

        for column, lags in lag_map.items():
            for lag in lags:
                combined[f"{column}_lag_{lag}"] = combined[column].shift(lag)

        return combined

    # ======================================================
    # DELTAS
    # ======================================================

    def create_delta_features(self, combined):
        delta_cols = [
            "pressure_bar",
            "temp_celsius",
            "flow_lpm",
            "vibration_magnitude"
        ]

        for col in delta_cols:
            combined[f"{col}_delta_1"] = combined[col].diff(1)

        return combined

    # ======================================================
    # ACCELERATION
    # ======================================================

    def create_acceleration_features(self, combined):
        cols = [
            "pressure_bar",
            "temp_celsius",
            "flow_lpm",
            "vibration_magnitude"
        ]

        for col in cols:
            combined[f"{col}_acceleration"] = combined[col].diff().diff()

        return combined

    # ======================================================
    # ROLLING FEATURES
    # ======================================================

    def create_rolling_features(self, combined):
        combined["vibration_magnitude_rolling_std_6"] = (
            combined["vibration_magnitude"].rolling(6).std()
        )

        combined["flow_lpm_rolling_std_6"] = (
            combined["flow_lpm"].rolling(6).std()
        )

        combined["pump_rpm_rolling_std_6"] = (
            combined["pump_rpm"].rolling(6).std()
        )

        combined["rolling_vibration_energy"] = (
            combined["vibration_magnitude"]
            .rolling(6)
            .apply(lambda x: np.sum(x ** 2), raw=True)
        )

        return combined

    def calculate_trend_slope(self, values):
        values = np.array(values)

        if len(values) < 2:
            return 0.0

        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        return float(slope)

    # ======================================================
    # TREND FEATURES
    # ======================================================

    def create_trend_features(self, combined):
        combined["vibration_magnitude_trend_slope_15"] = (
            combined["vibration_magnitude"]
            .rolling(15)
            .apply(self.calculate_trend_slope, raw=False)
        )

        combined["pressure_bar_trend_slope_15"] = (
            combined["pressure_bar"]
            .rolling(15)
            .apply(self.calculate_trend_slope, raw=False)
        )

        combined["temp_celsius_trend_slope_15"] = (
            combined["temp_celsius"]
            .rolling(15)
            .apply(self.calculate_trend_slope, raw=False)
        )

        return combined

    # ======================================================
    # BUILD MODEL INPUT
    # ======================================================

    def build_model_input(self, machine_df, sensor_input):
        combined = self.rebuild_features(machine_df, sensor_input)
        combined = self.create_lag_features(combined)
        combined = self.create_delta_features(combined)
        combined = self.create_acceleration_features(combined)
        combined = self.create_rolling_features(combined)
        combined = self.create_trend_features(combined)

        combined = combined.bfill()
        combined = combined.fillna(0)

        latest_row = combined.iloc[[-1]].copy()
        X = latest_row[self.feature_cols]

        return X

    # ======================================================
    # ASSET CONDITION
    # ======================================================

    def determine_asset_condition(self, predicted_rul):
        if predicted_rul <= 48:
            return {
                "risk_level": "CRITICAL",
                "priority": "IMMEDIATE ACTION REQUIRED"
            }
        elif predicted_rul <= 96:
            return {
                "risk_level": "WARNING",
                "priority": "SCHEDULE MAINTENANCE SOON"
            }
        elif predicted_rul <= 168:
            return {
                "risk_level": "CAUTION",
                "priority": "PLAN MAINTENANCE"
            }
        else:
            return {
                "risk_level": "NORMAL",
                "priority": "CONTINUE MONITORING"
            }

    # ======================================================
    # FAILURE PROGRESSION
    # ======================================================

    def determine_progression_stage(self, predicted_rul):
        if predicted_rul <= 48:
            return {
                "stage": "IMMINENT FAILURE",
                "narrative": (
                    "The identified failure mechanism "
                    "has progressed to a critical stage. "
                    "Remaining useful life is approaching "
                    "end-of-life thresholds and immediate "
                    "maintenance intervention is recommended."
                )
            }
        elif predicted_rul <= 96:
            return {
                "stage": "ADVANCING FAILURE",
                "narrative": (
                    "The degradation mechanism is actively "
                    "progressing and reducing remaining "
                    "useful life. Maintenance intervention "
                    "should be scheduled before the asset "
                    "enters a critical condition."
                )
            }
        elif predicted_rul <= 168:
            return {
                "stage": "DEVELOPING FAILURE",
                "narrative": (
                    "A measurable degradation pattern "
                    "has emerged and is becoming established. "
                    "Maintenance planning should begin to "
                    "prevent future operational impact."
                )
            }
        else:
            return {
                "stage": "EARLY FAILURE SIGNATURE",
                "narrative": (
                    "An early degradation signature has "
                    "been detected. The asset remains in a "
                    "healthy operating condition with "
                    "substantial useful life remaining. "
                    "Continued monitoring is recommended."
                )
            }

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(self, machine_id, sensor_input):
        machine_df = self.dataset[self.dataset["machine_id"] == machine_id]

        latest_machine_record = (

            machine_df

            .sort_values("timestamp")

            .iloc[-1]
        )

        equipment_age_days = float(

            latest_machine_record[
                "equipment_age_days"
            ]
        )

        days_since_filter_change = float(

            latest_machine_record[
                "days_since_filter_change"
            ]
        )

        days_since_last_maintenance = float(

            latest_machine_record[
                "days_since_last_maintenance"
            ]
        )

        if machine_df.empty:
            raise ValueError(f"Machine {machine_id} not found")

        # --------------------------------------------------
        # REBUILD FEATURES
        # --------------------------------------------------
        X = self.build_model_input(machine_df, sensor_input)

        # --------------------------------------------------
        # PREDICT
        # --------------------------------------------------
        predicted_rul_hours = float(self.model.predict(X)[0])
        predicted_rul_hours = max(0, predicted_rul_hours)
        predicted_rul_days = round(predicted_rul_hours / 24, 2)

        # ==================================================
        # MACHINE HEALTH SCORE
        # ==================================================

        machine_health_score = round(

            max(
                0,
                min(
                    100,
                    (predicted_rul_hours / 336) * 100
                )
            ),

            1
        )

        machine_health_score = max(
            0,
            min(
                100,
                machine_health_score
            )
        )

        # --------------------------------------------------
        # ASSET CONDITION
        # --------------------------------------------------
        asset_condition = self.determine_asset_condition(predicted_rul_hours)

        # --------------------------------------------------
        # FAILURE STAGE
        # --------------------------------------------------
        progression = self.determine_progression_stage(predicted_rul_hours)

        # --------------------------------------------------
        # SHAP EXPLAINABILITY
        # --------------------------------------------------
        try:
            shap_df = self.shap_explainer.explain(X)
            top_drivers = build_local_explanation(shap_df)
        except Exception:
            shap_df = pd.DataFrame()
            top_drivers = []

        # --------------------------------------------------
        # FAILURE PROFILE
        # --------------------------------------------------
        machine_profile = X.iloc[0].copy()
        machine_profile["predicted_rul"] = predicted_rul_hours
        (
            probability_df,
            failure_probability_table,
            signature_strength,
            pattern_strength,
        ) = self.failure_engine.calculate(
            machine_profile,
            self.failure_profiles,
            shap_df
        )

         # ==================================================
        # FAILURE SIGNATURE SCORE
        # ==================================================

        failure_signature_score = round(
            pattern_strength,
            1
        )

        pattern_analysis = generate_pattern_interpretation(
            probability_df,
            signature_strength
        )

        # --------------------------------------------------
        # TOP FAILURE MODE
        # --------------------------------------------------
        if probability_df.empty:
            failure_mode = "UNKNOWN"
            failure_probability = 0.0
            competing_pattern = "UNKNOWN"
        else:
            failure_mode = probability_df.iloc[0]["Failure_Mode"]
            failure_probability = float(probability_df.iloc[0]["Probability_%"])

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------
        recommendations = generate_recommendations(failure_mode)

        # --------------------------------------------------
        # EXECUTIVE NARRATIVE
        # --------------------------------------------------
        executive_summary = generate_narrative(

            predicted_rul_hours=predicted_rul_hours,

            predicted_rul_days=predicted_rul_days,

            failure_mode=failure_mode,

            failure_signature_strength=signature_strength,

            top_drivers=top_drivers,

            risk_level=asset_condition["risk_level"],

            progression_stage=progression["stage"]
        )

        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------
        return {
            "machine_id": machine_id,
            "predicted_rul_hours": round(predicted_rul_hours, 2),
            "predicted_rul_days": predicted_rul_days,
            "risk_level": asset_condition["risk_level"],
            "equipment_age_days": equipment_age_days,
            "days_since_filter_change": days_since_filter_change,
            "days_since_last_maintenance": days_since_last_maintenance,
            "top_drivers": top_drivers,
            "machine_health_score": machine_health_score,
            "priority": asset_condition["priority"],
            "failure_mode": failure_mode,
            "failure_mode_probabilities": failure_probability_table,
            "failure_signature_strength": signature_strength,
            "failure_progression_stage": progression["stage"],
            "failure_progression_narrative": progression["narrative"],
            "failure_pattern_analysis": pattern_analysis,
            "recommended_actions": recommendations,
            "executive_summary": executive_summary
        }
    