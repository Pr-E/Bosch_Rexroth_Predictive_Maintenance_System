from pydantic import BaseModel

from typing import List


# ======================================================
# INPUT
# ======================================================

class SensorInput(BaseModel):

    machine_id: str

    pressure_bar: float

    temp_celsius: float

    flow_lpm: float

    pump_rpm: float

    vibration_x_g: float

    vibration_y_g: float


# ======================================================
# SHAP DRIVERS
# ======================================================

class DriverExplanation(BaseModel):

    feature: str

    reason: str

    severity: str

    shap_impact: float


# ======================================================
# FAILURE MODE PROBABILITIES
# ======================================================

class FailureProbability(BaseModel):

    failure_mode: str

    probability_percent: float


# ======================================================
# FAILURE PATTERN INTELLIGENCE
# ======================================================

class FailurePatternAnalysis(BaseModel):

    dominant_failure: str

    pattern_strength: float

    competing_pattern: str

    failure_signature_strength: str

    interpretation: str


# ======================================================
# OUTPUT
# ======================================================

class PredictionResponse(BaseModel):

    machine_id: str

    predicted_rul_hours: float

    predicted_rul_days: float

    risk_level: str

    equipment_age_days: float

    days_since_filter_change: float

    days_since_last_maintenance: float

    top_drivers: (
        List[DriverExplanation]
    )

    priority: str

    machine_health_score: float

    failure_mode: str

    failure_signature_strength: str

    failure_progression_stage: str

    failure_progression_narrative: str

    failure_pattern_analysis: (
        FailurePatternAnalysis
    )

    failure_mode_probabilities: (
        List[FailureProbability]
    )

    recommended_actions: (
        List[str]
    )

    executive_summary: str