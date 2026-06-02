# Bosch Rexroth Predictive Maintenance Intelligence System

## Explainable Remaining Useful Life Prediction for Industrial Hydraulic Assets

### Overview

This project presents an end-to-end machine learning framework for predicting Remaining Useful Life (RUL) in industrial hydraulic systems while providing transparent explanations of degradation behaviour and operational risk.

The objective is to support maintenance planning by combining predictive modelling, explainable AI, and degradation pattern assessment into a unified decision-support workflow.

Rather than relying solely on failure prediction, the system is designed to help engineers understand:

* How much useful life remains
* Which operational factors are influencing asset health
* How degradation is evolving over time
* Which historical failure patterns the asset most closely resembles
* What maintenance actions may be appropriate

---

## Problem Statement

Hydraulic assets operate under varying environmental, operational, and maintenance conditions. Over time, factors such as thermal stress, vibration exposure, pressure imbalance, equipment ageing, and maintenance delays contribute to progressive degradation.

Traditional maintenance approaches often rely on fixed servicing schedules or reactive interventions, which may result in:

* Unplanned downtime
* Increased maintenance costs
* Reduced equipment availability
* Inefficient resource allocation

This project explores how machine learning can be used to support condition-based maintenance planning through Remaining Useful Life estimation and explainable degradation analysis.

---

## Solution Overview

The system consists of four integrated analytical layers.

### 1. Data Engineering

Multiple operational and maintenance data sources were integrated to create a unified asset lifecycle dataset.

Key activities included:

* Data ingestion
* Timestamp standardisation
* Asset-level aggregation
* Data quality validation
* Temporal alignment of operational records

---

### 2. Feature Engineering

Domain-informed features were developed to represent operational behaviour, maintenance history, and degradation progression.

Feature categories include:

#### Operational Features

* Pressure
* Temperature
* Flow Rate
* Pump Speed

#### Maintenance Features

* Equipment Age
* Days Since Last Maintenance
* Days Since Filter Change

#### Degradation Features

* Thermal Stress Accumulation
* Cumulative Vibration Exposure
* Downtime Exposure
* Pressure-Flow Ratio
* Thermal-Hydraulic Stress

#### Temporal Features

* Lag Variables
* Rolling Statistics
* Behavioural Trend Indicators

---

### 3. Remaining Useful Life Prediction

Gradient boosting regression models were evaluated for Remaining Useful Life estimation.

Models explored:

* XGBoost
* LightGBM

Evaluation metrics:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

The final modelling framework demonstrated strong predictive performance across multiple stages of asset degradation while maintaining temporal validation integrity.

---

### 4. Explainable AI and Maintenance Intelligence

SHAP (SHapley Additive Explanations) was incorporated to improve model transparency and support engineering interpretation.

For each prediction, the system identifies:

* Key degradation drivers
* Relative feature influence
* Asset-specific explanatory insights

Recurring contributors to reduced asset life included:

* Thermal stress accumulation
* Vibration exposure
* Hydraulic pressure-flow imbalance
* Equipment ageing
* Maintenance interval extension

---

### 5. Prognostic Intelligence Layer

The system extends beyond RUL prediction by introducing:

#### Failure Mode Profiling

Historical failure signatures are generated for:

* Pump Wear
* Cylinder Drift
* Valve Leakage
* Contamination

---

#### Failure Pattern Similarity Engine

Weighted similarity analysis compares live machine behaviour against historical failure signatures.

Example Output

```text
Pump Wear: 45%
Cylinder Drift: 23%
Valve Leakage: 19%
Contamination: 13%
```

#### Failure Signature Confidence

* High
* Moderate
* Emerging Pattern
* Low

---

#### Failure Progression Staging

| Stage                   | Remaining Useful Life |
| ----------------------- | --------------------- |
| Imminent Failure        | ≤ 48 Hours            |
| Advancing Failure       | 48 – 96 Hours         |
| Developing Failure      | 96 – 168 Hours        |
| Early Failure Signature | > 168 Hours           |

---



### Consistent Degradation Drivers

Across validation samples, the most influential degradation indicators were:

* Thermal stress accumulation
* Vibration accumulation
* Pressure-flow imbalance
* Equipment ageing
* Maintenance delay

These findings align with known industrial asset degradation mechanisms.

---

## Technology Stack

### Data Processing

* Python
* Pandas
* NumPy

### Machine Learning

* XGBoost
* LightGBM
* Scikit-learn

### Explainable AI

* SHAP

### Visualisation

* Matplotlib

### Deployment

* MLFLOW Tracking
* FastAPI
* Docker
* GitHub Actions
* AWS Services

---

## Repository Structure

```text
bosch-rexroth-predictive-maintenance/

├── data/
├── notebooks/
├── src/
│   ├── features/
│   ├── modelling/
│   ├── explainability/
│   ├── intelligence/
│   └── api/
├── models/
├── tests/
├── reports/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Current Status

Completed

* Data ingestion and integration
* Feature engineering
* Remaining Useful Life modelling
* Explainable AI framework
* Degradation pattern assessment
* Failure progression framework
* Validation and performance evaluation

In Progress

* Production API development
* Containerisation
* CI/CD automation
* Cloud deployment

---

## Future Enhancements

* Real-time telemetry integration
* Fleet-level health monitoring
* Maintenance scheduling optimisation

---

## Author

Priscilla Ejiro

Data Scientist | Machine Learning Engineer

Interests: Explainable AI, Predictive Maintenance, Reliability Engineering, Healthcare & Industrial Analytics


