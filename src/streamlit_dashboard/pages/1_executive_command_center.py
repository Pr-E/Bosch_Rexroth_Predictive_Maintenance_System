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
    page_title="Bosch Rexroth Command Center",
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

    business_values = [
        {
            "objective": "Predict Failures Early",
            "detail": "RUL prediction enables early intervention before failure."
        },
        {
            "objective": "Reduce Downtime",
            "detail": "Risk scoring supports proactive maintenance planning."
        },
        {
            "objective": "Optimise Maintenance",
            "detail": "Recommendations guide targeted maintenance actions."
        },
        {
            "objective": "Improve Asset Visibility",
            "detail": "Dashboard converts telemetry into executive intelligence."
        },
        {
            "objective": "Explainable AI Decisions",
            "detail": "SHAP highlights the main degradation drivers."
        },
        {
            "objective": "Support Industry 4.0",
            "detail": "FastAPI, Streamlit, MLflow and AWS enable production readiness."
        }
    ]

    for item in business_values:
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 0.7rem; min-height: 80px;">
                <div style="color:#22d3ee; font-weight:800; font-size:0.95rem;">
                    ✓ {item["objective"]}
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; margin-top:0.35rem;">
                    {item["detail"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    narrative_card(
        """
        The strongest predictive drivers are vibration exposure, thermal stress,
        maintenance intervals, hydraulic pressure-flow imbalance, and downtime exposure.
        These findings show that the model successfully learned meaningful physical
        degradation patterns associated with hydraulic system wear and provides a
        reliable foundation for predictive maintenance decision support.
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
        height=400,
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
        "Risk Level": [
            "CRITICAL",
            "WARNING",
            "CAUTION",
            "NORMAL"
        ],
        "Meaning": [
            "Immediate intervention required",
            "Schedule maintenance soon",
            "Plan maintenance",
            "Continue monitoring"
        ],
        "Assets": [2, 3, 2, 2]
    })

    fig = px.bar(
        rul_df,
        x="Stage",
        y="Assets",
        color="Risk Level",
        text="Risk Level",
        template="plotly_dark",
        color_discrete_map={
            "CRITICAL": "#ef4444",
            "WARNING": "#f97316",
            "CAUTION": "#eab308",
            "NORMAL": "#22c55e"
        },
        hover_data=["Meaning"]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="RUL Stage",
        yaxis_title="Assets"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="glass-card" style="margin-top:0.7rem;">
            <div style="color:#ef4444;"><b>CRITICAL:</b> 0–48 hrs | Immediate action required</div>
            <div style="color:#f97316;"><b>WARNING:</b> 48–96 hrs | Schedule maintenance soon</div>
            <div style="color:#eab308;"><b>CAUTION:</b> 96–168 hrs | Plan maintenance</div>
            <div style="color:#22c55e;"><b>NORMAL:</b> >168 hrs | Continue monitoring</div>
        </div>
        """,
        unsafe_allow_html=True
    )