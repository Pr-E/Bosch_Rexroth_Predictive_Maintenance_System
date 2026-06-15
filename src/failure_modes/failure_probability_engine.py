import numpy as np
import pandas as pd

from src.failure_modes.confidence_scoring import calculate_signature_strength


class FailureProbabilityEngine:

    def __init__(self):
        pass

    def calculate(self, machine_profile, failure_profiles, top_driver_df):
        if top_driver_df.empty:
            return (pd.DataFrame(), [], "UNKNOWN", 0.0, 0.0)

        # SHAP weights
        shap_weights = dict(zip(top_driver_df["Feature"], top_driver_df["Influence_Strength"]))
        total_weight = sum(abs(v) for v in shap_weights.values())
        if total_weight == 0:
            total_weight = 1
        shap_weights = {feature: abs(weight) / total_weight for feature, weight in shap_weights.items()}

        # Distance calculation
        distances = {}
        for mode, profile_data in failure_profiles.items():
            profile_median = profile_data["median"]
            profile_std = profile_data["std"]

            weighted_distances = []
            weights = []

            for feature in shap_weights:
                if feature not in machine_profile.index or feature not in profile_median:
                    continue

                machine_value = float(machine_profile[feature])
                profile_value = float(profile_median[feature])
                sigma = float(profile_std.get(feature, 1.0))

                z_distance = abs((machine_value - profile_value) / (sigma + 1e-6))
                weighted_distances.append(z_distance)
                weights.append(shap_weights[feature])

            if len(weighted_distances) == 0:
                continue

            distance = np.average(weighted_distances, weights=weights)
            distances[mode] = distance

        # Distance → probability
        inverse_scores = {mode: 1 / (distance + 1e-6) for mode, distance in distances.items()}
        total_score = sum(inverse_scores.values())
        probabilities = {mode: round(score / total_score * 100, 2) for mode, score in inverse_scores.items()}

        probability_df = pd.DataFrame({
            "Failure_Mode": probabilities.keys(),
            "Probability_%": probabilities.values()
        })
        probability_df = probability_df.sort_values("Probability_%", ascending=False).reset_index(drop=True)

        failure_probability_table = (
            probability_df
            .rename(columns={"Failure_Mode": "failure_mode", "Probability_%": "probability_percent"})
            .to_dict(orient="records")
        )

        # Signature strength
        signature_strength, pattern_strength, separation = calculate_signature_strength(probability_df)

        return (probability_df, failure_probability_table, signature_strength, float(pattern_strength))