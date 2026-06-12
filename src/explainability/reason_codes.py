REASON_CODE_MAP = {

    "thermal_stress_accumulation":
        "Accumulated thermal stress contributing to degradation",

    "cumulative_vibration_exposure":
        "Long-term vibration damage accumulation detected",

    "pressure_flow_ratio":
        "Hydraulic pressure-flow imbalance detected",

    "days_since_filter_change":
        "Filter servicing interval contributing to wear",

    "cumulative_downtime_exposure":
        "Operational downtime burden reducing asset reliability",

    "equipment_age_days":
        "Equipment ageing contributing to degradation",

    "days_since_last_maintenance":
        "Maintenance interval exceeds optimal servicing window",

    "rolling_vibration_energy":
        "Sustained vibration energy indicates progressive wear",

    "thermal_hydraulic_stress":
        "Combined thermal-hydraulic stress detected",

    "flow_lpm":
        "Historical hydraulic flow degradation detected",

    "pressure_bar":
        "Hydraulic pressure instability detected",

    "temp_celsius":
        "Elevated operating temperature contributing to wear",

    "pump_rpm":
        "Pump rotational performance degradation detected",

    "vibration_magnitude":
        "Elevated vibration magnitude detected",

    "vibration_magnitude_rolling_std_6":
        "Increasing vibration variability detected"
}


SEVERITY_EXPLANATIONS = {

    "CRITICAL":
        (
            "This factor is exerting severe influence "
            "on machine degradation and is materially "
            "reducing remaining useful life."
        ),

    "HIGH":
        (
            "This factor is significantly contributing "
            "to degradation and should be addressed."
        ),

    "MODERATE":
        (
            "This factor is contributing to wear and "
            "should be monitored."
        ),

    "LOW":
        (
            "This factor is currently having limited "
            "impact on degradation."
        ),

    "MINIMAL":
        (
            "This factor is presently contributing "
            "very little to overall degradation."
        )
}