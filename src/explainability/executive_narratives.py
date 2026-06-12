# ==========================================================
# EXECUTIVE NARRATIVE ENGINE
# ==========================================================

def generate_narrative(

    predicted_rul_hours,
    predicted_rul_days,
    failure_mode,
    failure_signature_strength,
    top_drivers,
    risk_level,
    progression_stage

):
    """
    Executive AI Narrative

    Business-facing explanation of the
    current machine condition.
    """

    # ------------------------------------------------------
    # DRIVER SUMMARY
    # ------------------------------------------------------

    if len(top_drivers) > 0:

        driver_summary = ", ".join(

            [

                driver["reason"]

                for driver

                in top_drivers[:3]

            ]

        )

    else:

        driver_summary = (

            "no significant degradation drivers identified"
        )

    # ------------------------------------------------------
    # NARRATIVE
    # ------------------------------------------------------

    narrative = (

        f"The hydraulic asset is currently assessed as "
        f"{risk_level} with an estimated remaining useful "
        f"life of {predicted_rul_hours:.1f} hours "
        f"({predicted_rul_days:.1f} days). "

        f"The dominant degradation pattern currently "
        f"resembles {failure_mode.replace('_', ' ')}. "

        f"The asset is classified within the "
        f"'{progression_stage}' stage of failure progression. "

        f"Primary contributing factors include "
        f"{driver_summary}. "

        f"The detected failure signature is currently "
        f"classified as '{failure_signature_strength}'. "

        f"Maintenance teams should prioritise actions "
        f"aligned with the identified degradation pathway "
        f"to minimise operational risk and prevent "
        f"unplanned downtime."
    )

    return narrative




# ==========================================================
# FAILURE PATTERN INTERPRETATION
# ==========================================================
def generate_pattern_interpretation(

    probability_df,

    signature_strength

):

    if probability_df.empty:

        return {}

    dominant_failure = (

        probability_df
        .iloc[0]["Failure_Mode"]
    )

    dominant_probability = (

        probability_df
        .iloc[0]["Probability_%"]
    )

    if len(probability_df) > 1:

        competing_failure = (

            probability_df
            .iloc[1]["Failure_Mode"]
        )

    else:

        competing_failure = "NONE"

    if signature_strength == "DOMINANT SIGNATURE":

        interpretation = (

            f"A clear {dominant_failure.replace('_',' ')} "
            f"degradation signature has been identified. "
            f"The asset strongly resembles historical "
            f"{dominant_failure.replace('_',' ')} failure "
            f"behaviour with limited evidence of competing "
            f"failure mechanisms."
        )

    elif signature_strength == "ESTABLISHED SIGNATURE":

        interpretation = (

            f"The asset most closely resembles "
            f"{dominant_failure.replace('_',' ')} "
            f"degradation behaviour. Some characteristics "
            f"of {competing_failure.replace('_',' ')} "
            f"are also present, suggesting overlap between "
            f"potential degradation pathways."
        )

    elif signature_strength == "EMERGING SIGNATURE":

        interpretation = (

            f"An emerging "
            f"{dominant_failure.replace('_',' ')} "
            f"degradation signature has been detected. "
            f"Multiple failure mechanisms remain plausible "
            f"and continued monitoring is recommended."
        )

    else:

        interpretation = (

            f"No dominant degradation mechanism has yet "
            f"been established. Additional operational "
            f"evidence is required before a definitive "
            f"failure pathway can be confirmed."
        )

    return {

        "dominant_failure":
            dominant_failure,

        "pattern_strength":
            float(dominant_probability),

        "competing_pattern":
            competing_failure,

        "failure_signature_strength":
            signature_strength,

        "interpretation":
            interpretation
    }