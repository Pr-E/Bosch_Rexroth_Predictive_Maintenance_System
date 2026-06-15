from fastapi import FastAPI, HTTPException

from src.api.routes import router
from src.pipeline.training import TrainingPipeline
from src.api.dashboard_service import DashboardKPIService
from src.logger import configure_logger

logging = configure_logger()

# ==========================================================
# FASTAPI APP
# ==========================================================
app = FastAPI(
    title="Bosch Rexroth Hydraulic Intelligence Platform",
    version="1.0.0",
    description="""
    Executive Hydraulic Asset Intelligence Platform

    Capabilities

    • Remaining Useful Life Prediction

    • Failure Pattern Recognition

    • Failure Signature Analysis

    • Failure Progression Intelligence

    • SHAP Explainability

    • Executive Maintenance Recommendations

    • Machine Health Scoring

    • Executive Narratives

    • Model Governance & Monitoring
    """
)

# ==========================================================
# STARTUP EVENT
# ==========================================================
@app.on_event("startup")
def startup_event():
    logging.info("=" * 60)
    logging.info("Bosch Rexroth API Started")
    logging.info("=" * 60)

# ==========================================================
# ROUTES
# ==========================================================
app.include_router(router, prefix="/api", tags=["Prediction"])

# ==========================================================
# HOME
# ==========================================================
@app.get("/")
def home():
    return {
        "platform": "Bosch Rexroth Hydraulic Intelligence Platform",
        "version": "1.0.0",
        "status": "running"
    }

# ==========================================================
# HEALTH CHECK
# ==========================================================
@app.get("/health")
def health():
    return {"status": "healthy"}

# ==========================================================
# SYSTEM INFO
# ==========================================================
@app.get("/info")
def info():
    return {
        "project": "Bosch Rexroth Predictive Maintenance",
        "capabilities": [
            "RUL Prediction",
            "Failure Pattern Recognition",
            "Failure Signature Intelligence",
            "Failure Progression Intelligence",
            "SHAP Explainability",
            "Machine Health Scoring",
            "Maintenance Recommendations",
            "Executive Narratives"
        ]
    }

# ==========================================================
# MODEL RETRAINING
# ==========================================================
@app.post("/train")
def train_model():
    pipeline = TrainingPipeline()
    pipeline.train()
    return {
        "status": "success",
        "message": "Model retrained, versioned, uploaded and backed up."
    }

# ==========================================================
# EXECUTIVE DASHBOARD KPIs (singleton)
# ==========================================================
dashboard_service = DashboardKPIService()

@app.get("/api/dashboard/executive-kpi")
def executive_kpi():
    """
    Returns all executive KPIs computed LIVE from:
    - the S3 feature store
    - the latest model training summary (saved during training)
    """
    return dashboard_service.get_kpis()