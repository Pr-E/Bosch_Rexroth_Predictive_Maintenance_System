import pandas as pd


def calculate_signature_strength(probability_df: pd.DataFrame):
    if probability_df.empty:
        return ("UNKNOWN", 0.0, 0.0)

    dominant_probability = float(probability_df.iloc[0]["Probability_%"])

    if len(probability_df) > 1:
        competing_probability = float(probability_df.iloc[1]["Probability_%"])
    else:
        competing_probability = 0.0

    separation = round(dominant_probability - competing_probability, 2)

    if separation >= 35:
        signature_strength = "Clear Failure Pattern"
    elif separation >= 20:
        signature_strength = "Advancing Failure Pattern"
    elif separation >= 10:
        signature_strength = "Developing Failure Pattern"
    else:
        signature_strength = "Multiple Failure Indication"

    return (signature_strength, dominant_probability, separation)