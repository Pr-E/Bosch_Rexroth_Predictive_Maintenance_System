import streamlit as st

from utils.api_clients import retrain_model
from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card
)


st.set_page_config(
    page_title="Model Retraining",
    layout="wide"
)

load_css()

page_header(
    "Model",
    "Retraining Center",
    "Lifecycle management for maintaining model freshness, governance and production readiness."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Current Version", "v22", "MLflow registry")

with c2:
    kpi_card("Model Type", "LightGBM", "RUL regression")

with c3:
    kpi_card("R² Score", "0.902", "Latest validation")

with c4:
    kpi_card("Deployment", "Production", "API active")

st.markdown("<br>", unsafe_allow_html=True)

section_label("Retraining Workflow")

narrative_card(
    """
    Retraining executes the complete production pipeline: loading the latest
    feature store, rebuilding features, validating data, training LightGBM,
    evaluating MAE/RMSE/R², registering the model in MLflow and backing up
    artifacts to Amazon S3.
    """
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Start Production Retraining", use_container_width=True):
    with st.spinner("Retraining model. This may take several minutes..."):
        try:
            response = retrain_model()
            st.success(response.get("message", "Retraining completed."))
        except Exception as error:
            st.error(f"Retraining failed: {error}")

st.markdown("<br>", unsafe_allow_html=True)

section_label("Governance Controls")

st.success("Version controlled training pipeline")
st.success("MLflow experiment tracking")
st.success("Amazon S3 artifact backup")
st.success("FastAPI production retraining endpoint")
st.success("Executive monitoring through Streamlit")