import pandas as pd
import plotly.express as px
import streamlit as st

from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card,
    feature_importance_chart
)


st.set_page_config(
    page_title="Executive Command Center",
    layout="wide"
)

load_css()

page_header(
    "Executive Command",
    "Center",
    "Strategic overview of model performance, degradation intelligence and business value delivered."
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    kpi_card("Degraded Machines", "9", "Assets modelled")
with c2:
    kpi_card("Telemetry Records", "126,585", "Processed signals")
with c3:
    kpi_card("Features", "35", "Engineered predictors")
with c4:
    kpi_card("Average RUL", "112 hrs", "Operational estimate")
with c5:
    kpi_card("R² Score", "0.902", "Model fit")
with c6:
    kpi_card("MAE", "14.24 hrs", "Prediction error")

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    section_label("Executive Feature Importance")
    st.plotly_chart(
        feature_importance_chart(),
        use_container_width=True
    )

with right:
    section_label("Business Value Delivered")

    value_df = pd.DataFrame({
        "Objective": [
            "Predict Failures Early",
            "Reduce Downtime",
            "Optimise Maintenance Planning",
            "Improve Asset Visibility",
            "Explainable AI Decisions",
            "Support Industry 4.0"
        ],
        "Status": [
            "Achieved",
            "Achieved",
            "Achieved",
            "Achieved",
            "Achieved",
            "Achieved"
        ]
    })

    st.dataframe(
        value_df,
        use_container_width=True,
        hide_index=True
    )

    narrative_card(
        """
        The strongest predictive drivers are vibration exposure, thermal stress,
        maintenance intervals and hydraulic pressure-flow imbalance. These align
        directly with Bosch Rexroth's objective of moving from reactive maintenance
        to condition-based reliability intelligence.
        """
    )

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    section_label("Failure Pattern Distribution")

    mode_df = pd.DataFrame({
        "Failure Pattern": [
            "Pump Wear",
            "Valve Leakage",
            "Contamination",
            "Cylinder Drift"
        ],
        "Share": [34, 27, 31, 8]
    })

    fig = px.pie(
        mode_df,
        names="Failure Pattern",
        values="Share",
        hole=0.62,
        template="plotly_dark"
    )

    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with col_b:
    section_label("RUL Distribution")

    rul_df = pd.DataFrame({
        "Stage": [
            "0-48 hrs",
            "48-96 hrs",
            "96-168 hrs",
            ">168 hrs"
        ],
        "Assets": [2, 3, 2, 2]
    })

    fig = px.bar(
        rul_df,
        x="Stage",
        y="Assets",
        template="plotly_dark"
    )

    fig.update_traces(marker_color="#22d3ee")

    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)