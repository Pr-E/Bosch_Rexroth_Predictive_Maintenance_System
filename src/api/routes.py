from fastapi import APIRouter

from src.api.schemas import (
    SensorInput,
    PredictionResponse
)

from src.pipeline.prediction import (
    PredictionService
)

# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter()

# ==========================================================
# LOAD PREDICTION SERVICE ONCE
# ==========================================================

service = PredictionService()

# ==========================================================
# PREDICT
# ==========================================================

@router.post("/predict", response_model=PredictionResponse)
def predict_machine(data: SensorInput):
       return service.predict(

            machine_id=data.machine_id,

            sensor_input={

                "pressure_bar": data.pressure_bar,

                "temp_celsius": data.temp_celsius,

                "flow_lpm": data.flow_lpm,

                "pump_rpm": data.pump_rpm,

                "vibration_x_g": data.vibration_x_g,

                "vibration_y_g": data.vibration_y_g
            }
        )