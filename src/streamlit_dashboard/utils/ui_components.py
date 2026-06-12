import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DARK_TEMPLATE = "plotly_dark"


def page_header(title: str, accent: str, subtitle: str):
    st.markdown(
        f"""
        <div class="page-title">{title} <span>{accent}</span></div>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def section_label(text: str):
    st.markdown(
        f"<div class='section-label'>{text}</div>",
        unsafe_allow_html=True
    )


def kpi_card(label: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def narrative_card(text: str):
    st.markdown(
        f"""
        <div class="narrative-card">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def risk_badge(risk: str):
    css = {
        "CRITICAL": "badge-critical",
        "WARNING": "badge-warning",
        "CAUTION": "badge-caution",
        "NORMAL": "badge-normal",
    }.get(risk, "badge-normal")

    st.markdown(
        f"<span class='badge {css}'>{risk}</span>",
        unsafe_allow_html=True
    )


def health_gauge(score: float):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%"},
            title={"text": "Machine Health"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#22d3ee"},
                "steps": [
                    {"range": [0, 25], "color": "rgba(239,68,68,0.25)"},
                    {"range": [25, 55], "color": "rgba(249,115,22,0.22)"},
                    {"range": [55, 80], "color": "rgba(234,179,8,0.20)"},
                    {"range": [80, 100], "color": "rgba(34,197,94,0.22)"},
                ],
            },
        )
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(color="#f8fafc")
    )
    return fig


def failure_probability_chart(probabilities: list):
    df = pd.DataFrame(probabilities)

    if df.empty:
        return go.Figure()

    df["failure_mode"] = (
        df["failure_mode"]
        .str.replace("_", " ")
        .str.title()
    )

    fig = px.bar(
        df.sort_values("probability_percent"),
        x="probability_percent",
        y="failure_mode",
        orientation="h",
        text="probability_percent",
        template=DARK_TEMPLATE
    )

    fig.update_traces(
        marker_color="#22d3ee",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Pattern Strength (%)",
        yaxis_title="",
        margin=dict(l=20, r=30, t=30, b=30),
        font=dict(color="#f8fafc")
    )

    return fig


def shap_driver_chart(drivers: list):
    df = pd.DataFrame(drivers)

    if df.empty:
        return go.Figure()

    df["feature"] = (
        df["feature"]
        .str.replace("_", " ")
        .str.title()
    )

    severity_colors = {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MODERATE": "#eab308",
        "LOW": "#38bdf8",
        "MINIMAL": "#94a3b8",
    }

    fig = px.bar(
        df.sort_values("shap_impact"),
        x="shap_impact",
        y="feature",
        color="severity",
        color_discrete_map=severity_colors,
        orientation="h",
        template=DARK_TEMPLATE
    )

    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="SHAP Impact",
        yaxis_title="",
        margin=dict(l=20, r=20, t=30, b=30),
        font=dict(color="#f8fafc")
    )

    return fig


def feature_importance_chart():
    df = pd.DataFrame({
        "Feature": [
            "Cumulative Vibration Exposure",
            "Thermal Stress Accumulation",
            "Days Since Last Maintenance",
            "Cumulative Downtime Exposure",
            "Pressure Flow Ratio",
            "Equipment Age Days",
            "Days Since Filter Change",
            "Thermal Hydraulic Stress",
            "Rolling Vibration Energy",
            "Flow LPM Lag 6",
        ],
        "Importance": [
            2331, 2130, 2008, 1438, 1361,
            1221, 930, 862, 463, 377
        ]
    })

    fig = px.bar(
        df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        template=DARK_TEMPLATE
    )

    fig.update_traces(marker_color="#22d3ee")

    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Importance",
        yaxis_title="",
        margin=dict(l=20, r=20, t=30, b=30),
        font=dict(color="#f8fafc")
    )

    return fig