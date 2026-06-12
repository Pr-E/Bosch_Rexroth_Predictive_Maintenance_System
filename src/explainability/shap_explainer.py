import shap
import pandas as pd


class ShapExplainer:

    def __init__(

        self,

        model

    ):

        self.model = model

        self.explainer = (

            shap.TreeExplainer(
                model
            )
        )

    def explain(

        self,

        X

    ):

        shap_values = (

            self.explainer

            .shap_values(X)
        )

        explanation_df = pd.DataFrame({

            "Feature":
                X.columns,

            "SHAP_Value":
                shap_values[0]

        })

        explanation_df[

            "Influence_Strength"

        ] = (

            explanation_df[
                "SHAP_Value"
            ]

            .abs()
        )

        explanation_df = (

            explanation_df

            .sort_values(

                "Influence_Strength",

                ascending=False
            )

            .reset_index(
                drop=True
            )
        )

        return explanation_df.head(10)