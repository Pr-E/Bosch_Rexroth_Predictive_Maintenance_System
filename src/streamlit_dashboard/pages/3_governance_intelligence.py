import pandas as pd
import streamlit as st
from pathlib import Path

from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card
)


st.set_page_config(
    page_title="Governance Intelligence",
    layout="wide"
)

load_css()

BASE_DIR = Path(__file__).resolve().parents[1]
USER_FLOW_PATH = BASE_DIR / "assets" / "user_flow.png"

page_header(
    "Governance &",
    "Production Intelligence",
    "Enterprise readiness, model governance, deployment architecture and technology stack."
)

# ======================================================
# TOP KPIS
# ======================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Production Model", "LightGBM", "RUL regressor")

with c2:
    kpi_card("Model Version", "v22", "MLflow registry")

with c3:
    kpi_card("R² Score", "0.902", "Validated performance")

with c4:
    kpi_card("MAE", "14.24 hrs", "Prediction error")

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# TECHNOLOGY STACK
# ======================================================

section_label("Technology Stack")

tech_items = [
    ("Development", "VS Code", "Production development"),
    ("Data Processing", "Pandas / NumPy", "Telemetry preparation"),
    ("Feature Engineering", "Python Pipeline", "Maintenance and temporal features"),
    ("Model Training", "LightGBM / XGBoost", "RUL prediction"),
    ("Experiment Tracking", "MLflow + DagsHub", "Metrics and model registry"),
    ("Artifact Storage", "Amazon S3", "Models, metadata and feature store"),
    ("API Serving", "FastAPI", "Prediction and retraining endpoints"),
    ("Dashboard", "Streamlit", "Executive intelligence interface"),
    ("CI/CD", "GitHub Actions / Docker", "Automated deployment"),
    ("Cloud Runtime", "AWS EC2 / ECR", "Scalable production hosting"),
]

cols = st.columns(5)

for idx, item in enumerate(tech_items):
    layer, tech, purpose = item

    with cols[idx % 5]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:150px; margin-bottom:1rem;">
                <div style="color:#22d3ee; font-size:0.78rem; letter-spacing:0.16rem; text-transform:uppercase; font-weight:800;">
                    {layer}
                </div>
                <div style="color:white; font-size:1.25rem; font-weight:800; margin-top:0.65rem;">
                    {tech}
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-top:0.55rem; line-height:1.45;">
                    {purpose}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# END-TO-END FLOW IMAGE
# ======================================================

section_label("End-to-End Production Flow")

narrative_card(
    """
    Telemetry sensor data is transformed into degradation-focused features.
    The LightGBM model predicts Remaining Useful Life, SHAP explains local
    drivers, and the failure profile engine identifies dominant failure
    patterns. FastAPI serves predictions to the Streamlit executive command
    center, with MLflow and Amazon S3 supporting governance, versioning and
    production traceability.
    """
)

st.markdown("<br>", unsafe_allow_html=True)

if USER_FLOW_PATH.exists():
    st.image(
        str(USER_FLOW_PATH),
        use_container_width=True
    )
else:
    st.warning(
        "user_flow.png not found in assets folder. "
        "Please save the image as src/streamlit_dashboard/assets/user_flow.png"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# GOVERNANCE CONTROLS
# ======================================================

section_label("Governance Controls")

governance_items = [
    ("Model Registry", "Implemented", "Registered model versions tracked through MLflow."),
    ("Experiment Tracking", "Implemented", "Metrics, parameters and artifacts logged."),
    ("Feature Metadata", "Implemented", "Production feature list stored and reused."),
    ("S3 Backup", "Implemented", "Models and artifacts backed up to Amazon S3."),
    ("FastAPI Health Check", "Implemented", "API readiness monitored through health endpoint."),
    ("Retraining Endpoint", "Implemented", "Model retraining available through production API."),
    ("Explainability Layer", "Implemented", "SHAP driver intelligence supports transparent predictions."),
    ("Executive Narrative Layer", "Implemented", "Business-facing summaries generated automatically."),
]

g1, g2, g3, g4 = st.columns(4)

for idx, item in enumerate(governance_items):
    control, status, description = item

    with [g1, g2, g3, g4][idx % 4]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:145px; margin-bottom:1rem;">
                <div style="color:#22d3ee; font-weight:800; font-size:1rem;">
                    ✓ {control}
                </div>
                <div style="color:#22c55e; font-size:0.82rem; font-weight:800; margin-top:0.45rem;">
                    {status}
                </div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-top:0.55rem; line-height:1.45;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )