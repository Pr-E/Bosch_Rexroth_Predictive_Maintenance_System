import pandas as pd
import streamlit as st

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

page_header(
    "Governance &",
    "Production Intelligence",
    "Enterprise readiness, model governance, deployment architecture and technology stack."
)

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

section_label("Technology Stack")

tech_df = pd.DataFrame({
    "Layer": [
        "Development",
        "Data Processing",
        "Feature Engineering",
        "Model Training",
        "Experiment Tracking",
        "Artifact Storage",
        "API Serving",
        "Dashboard",
        "CI/CD",
        "Cloud Runtime"
    ],
    "Technology": [
        "VS Code",
        "Pandas / NumPy",
        "Python Feature Pipeline",
        "LightGBM / XGBoost",
        "MLflow + DagsHub",
        "Amazon S3",
        "FastAPI",
        "Streamlit",
        "GitHub Actions / Docker",
        "AWS EC2 / ECR"
    ],
    "Purpose": [
        "Production development",
        "Telemetry processing",
        "Maintenance and temporal features",
        "RUL prediction",
        "Metrics and model registry",
        "Models, metadata and feature store",
        "Prediction and retraining endpoints",
        "Executive intelligence interface",
        "Automated deployment",
        "Scalable production hosting"
    ]
})

st.dataframe(
    tech_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

section_label("End-to-End Production Flow")

narrative_card(
    """
    Telemetry sensor data is ingested and transformed into degradation-focused
    features. The LightGBM model predicts Remaining Useful Life, while SHAP
    explains local drivers and the failure profile engine identifies the dominant
    failure pattern. FastAPI serves predictions to the Streamlit executive command
    center, with MLflow and Amazon S3 supporting governance, versioning and
    production traceability.
    """
)

st.markdown("<br>", unsafe_allow_html=True)

governance_df = pd.DataFrame({
    "Governance Control": [
        "Model Registry",
        "Experiment Tracking",
        "Feature Metadata",
        "S3 Backup",
        "FastAPI Health Check",
        "Retraining Endpoint",
        "Explainability Layer",
        "Executive Narrative Layer"
    ],
    "Status": [
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented"
    ]
})

st.dataframe(
    governance_df,
    use_container_width=True,
    hide_index=True
)
