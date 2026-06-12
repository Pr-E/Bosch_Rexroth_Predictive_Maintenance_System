import streamlit as st

from utils.api_clients import predict_asset
from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card,
    risk_badge,
    health_gauge,
    failure_probability_chart,
    shap_driver_chart
)


st.set_page_config(
    page_title="Asset Intelligence",
    layout="wide"
)

load_css()

page_header(
    "Asset",
    "Intelligence",
    "Live RUL prediction, failure pattern recognition, SHAP explainability and maintenance actions."
)

left, right = st.columns([0.95, 1.45])

with left:
    section_label("Sensor Input")

    machine_id = st.selectbox(
        "Machine ID",
        [
            "HPU_01", "HPU_02", "HPU_03",
            "HPU_04", "HPU_05", "HPU_06",
            "HPU_07", "HPU_08", "HPU_09"
        ],
        index=2
    )

    pressure_bar = st.number_input("Pressure (bar)", value=115.0)
    temp_celsius = st.number_input("Temperature (°C)", value=52.0)
    flow_lpm = st.number_input("Flow (lpm)", value=88.0)
    pump_rpm = st.number_input("Pump RPM", value=1473.0)
    vibration_x_g = st.number_input("Vibration X (g)", value=0.35)
    vibration_y_g = st.number_input("Vibration Y (g)", value=0.35)

    run_prediction = st.button(
        "Generate Asset Intelligence",
        use_container_width=True
    )

with right:
    section_label("Prediction Result")

    if not run_prediction:
        narrative_card(
            """
            Awaiting sensor input. Select a hydraulic asset, enter the latest
            telemetry readings and run the intelligence engine.
            """
        )

if run_prediction:
    payload = {
        "machine_id": machine_id,
        "pressure_bar": pressure_bar,
        "temp_celsius": temp_celsius,
        "flow_lpm": flow_lpm,
        "pump_rpm": pump_rpm,
        "vibration_x_g": vibration_x_g,
        "vibration_y_g": vibration_y_g,
    }

    try:
        result = predict_asset(payload)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi_card(
                "Remaining Useful Life",
                f"{result['predicted_rul_hours']} hrs",
                f"{result['predicted_rul_days']} days"
            )

        with c2:
            kpi_card(
                "Machine Health",
                f"{result['machine_health_score']}%",
                "RUL-based health score"
            )

        with c3:
            kpi_card(
                "Failure Pattern",
                result["failure_mode"].replace("_", " ").title(),
                result["failure_signature_strength"]
            )

        with c4:
            kpi_card(
                "Priority",
                result["priority"],
                result["risk_level"]
            )

        st.markdown("<br>", unsafe_allow_html=True)

        g1, g2 = st.columns([0.85, 1.4])

        with g1:
            st.plotly_chart(
                health_gauge(result["machine_health_score"]),
                use_container_width=True
            )

            risk_badge(result["risk_level"])

        with g2:
            section_label("Failure Pattern Intelligence")

            pattern = result["failure_pattern_analysis"]

            k1, k2, k3 = st.columns(3)

            with k1:
                kpi_card(
                    "Dominant Pattern",
                    pattern["dominant_failure"].replace("_", " ").title()
                )

            with k2:
                kpi_card(
                    "Pattern Strength",
                    f"{pattern['pattern_strength']}%"
                )

            with k3:
                kpi_card(
                    "Competing Pattern",
                    pattern["competing_pattern"].replace("_", " ").title()
                )

            narrative_card(pattern["interpretation"])

        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)

        with m1:
            kpi_card(
                "Equipment Age",
                f"{int(result['equipment_age_days'])} days"
            )

        with m2:
            kpi_card(
                "Filter Change",
                f"{int(result['days_since_filter_change'])} days"
            )

        with m3:
            kpi_card(
                "Last Maintenance",
                f"{int(result['days_since_last_maintenance'])} days"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        p1, p2 = st.columns([1, 1.2])

        with p1:
            section_label("Failure Progression")
            kpi_card(
                "Progression Stage",
                result["failure_progression_stage"],
                result["risk_level"]
            )
            narrative_card(result["failure_progression_narrative"])

        with p2:
            section_label("Failure Mode Distribution")
            st.plotly_chart(
                failure_probability_chart(
                    result["failure_mode_probabilities"]
                ),
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        section_label("Primary SHAP Drivers")
        st.plotly_chart(
            shap_driver_chart(result["top_drivers"]),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        a1, a2 = st.columns([0.85, 1.15])

        with a1:
            section_label("Recommended Actions")
            for action in result["recommended_actions"]:
                st.success(action)

        with a2:
            section_label("Machine Health Summary")
            narrative_card(result["executive_summary"])

    except Exception as error:
        st.error(f"Prediction failed: {error}")