# src/streamlit_dashboard/app.py

from pathlib import Path

import streamlit as st

from utils.api_clients import check_api_health
from utils.styling import load_css
from utils.ui_components import page_header, kpi_card, narrative_card


st.set_page_config(
    page_title="Bosch Rexroth Intelligence",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "bosch_logo.png"


with st.sidebar:

    if LOGO_PATH.exists():
        st.image(
            str(LOGO_PATH),
            use_container_width=True
        )

    st.markdown("### HYDRAULIC SYSTEM")
    st.caption("PREDICTIVE MAINTENANCE INTELLIGENCE")

    st.divider()

    st.markdown("#### API STATUS")

    if check_api_health():
        st.success("ONLINE")
    else:
        st.error("OFFLINE")

    st.divider()

    st.markdown("#### NAVIGATION")
    st.caption("Use the pages menu above.")


page_header(
    "Hydraulic Predictive",
    "Maintenance Intelligence",
    "Executive Industrial Intelligence Command Center for Bosch Rexroth AG."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Telemetry Records",
        "126,585",
        "Degraded records processed"
    )

with c2:
    kpi_card(
        "Assets Monitored",
        "9",
        "Hydraulic power units"
    )

with c3:
    kpi_card(
        "Features Engineered",
        "35",
        "Degradation-focused signals"
    )

with c4:
    kpi_card(
        "Production Model",
        "LightGBM",
        "R² = 0.902"
    )

st.markdown("<br>", unsafe_allow_html=True)

narrative_card(
    """
    This platform converts hydraulic telemetry into executive-ready predictive
    maintenance intelligence. It predicts Remaining Useful Life, identifies
    failure patterns, explains degradation drivers using SHAP, and recommends
    maintenance actions through a FastAPI-powered intelligence layer.
    """
)