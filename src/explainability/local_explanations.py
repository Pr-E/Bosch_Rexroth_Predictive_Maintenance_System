from src.explainability.reason_codes import (
    REASON_CODE_MAP
)

from src.explainability.severity_engine import (
    determine_severity
)


def build_local_explanation(

    top_driver_df,

    top_n=10

):

    explanations = []

    for _, row in (

        top_driver_df

        .head(top_n)

        .iterrows()
    ):

        feature = row["Feature"]

        shap_impact = round(

            abs(

                row[
                    "Influence_Strength"
                ]

            ),

            3
        )

        severity = (

            determine_severity(
                shap_impact
            )
        )

        reason = (

            REASON_CODE_MAP.get(

                feature,

                feature
            )
        )

        explanations.append({

            "feature":
                feature,

            "reason":
                reason,

            "severity":
                severity,

            "shap_impact":
                shap_impact
        })

    return explanations




# ==========================================================
# FAILURE PATTERN INTERPRETATION
# ==========================================================

def generate_pattern_interpretation(

    probability_df,

    signature_strength

):

    if len(probability_df) < 2:

        return {}

    dominant_failure = (

        probability_df

        .iloc[0]

        ["Failure_Mode"]
    )

    dominant_probability = (

        probability_df

        .iloc[0]

        ["Probability_%"]
    )

    competing_failure = (

        probability_df

        .iloc[1]

        ["Failure_Mode"]
    )

    competing_probability = (

        probability_df

        .iloc[1]

        ["Probability_%"]
    )

    pattern_separation = round(

        dominant_probability

        -

        competing_probability,

        2
    )

    # ------------------------------------------------------
    # INTERPRETATION
    # ------------------------------------------------------

    if signature_strength == "STRONG SIGNATURE":

        interpretation = (

            f"A clear {dominant_failure.replace('_', ' ')} "
            f"degradation signature has been identified. "
            f"The asset strongly resembles historical "
            f"{dominant_failure.replace('_', ' ')} failure "
            f"behaviour with limited evidence of competing "
            f"failure mechanisms."
        )

    elif signature_strength == "ESTABLISHED SIGNATURE":

        interpretation = (

            f"The asset most closely resembles "
            f"{dominant_failure.replace('_', ' ')} "
            f"degradation behaviour. Some characteristics "
            f"of {competing_failure.replace('_', ' ')} "
            f"are also present, suggesting partial overlap "
            f"between degradation pathways."
        )

    elif signature_strength == "EMERGING SIGNATURE":

        interpretation = (

            f"An emerging "
            f"{dominant_failure.replace('_', ' ')} "
            f"degradation signature has been detected. "
            f"Multiple failure mechanisms remain plausible "
            f"and additional operational evidence may help "
            f"confirm future degradation progression."
        )

    else:

        interpretation = (

            f"The current degradation pattern does not yet "
            f"strongly resemble a single historical failure "
            f"mechanism. Continued monitoring is recommended "
            f"to establish a clearer degradation signature."
        )

    return {

        "dominant_failure":

            dominant_failure,

        "pattern_strength":

            dominant_probability,

        "competing_pattern":

            competing_failure,

        "pattern_separation":

            pattern_separation,

        "failure_signature_strength":

            signature_strength,

        "interpretation":

            interpretation
    }