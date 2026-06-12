FAILURE_ACTIONS = {

    "pump_wear": [

        "Inspect pump bearings",

        "Inspect rotating assemblies",

        "Review vibration trend",

        "Schedule pump maintenance"
    ],

    "valve_leakage": [

        "Inspect valve seals",

        "Pressure leak testing",

        "Review flow anomalies"
    ],

    "contamination": [

        "Replace hydraulic filters",

        "Inspect fluid condition",

        "Perform contamination analysis"
    ],

    "cylinder_drift": [

        "Inspect cylinder seals",

        "Check actuator performance",

        "Verify hydraulic pressure"
    ]
}


def generate_recommendations(

    failure_mode
):

    return FAILURE_ACTIONS.get(

        failure_mode,

        [

            "Perform detailed inspection"
        ]
    )