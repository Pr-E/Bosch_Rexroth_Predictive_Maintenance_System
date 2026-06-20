# Bosch Rexroth Predictive Maintenance Intelligence System

## Explainable Remaining Useful Life Prediction for Industrial Hydraulic Assets

### Overview

The Hydraulic Predictive Maintenance Intelligence System is a production-ready end-to-end machine learning and MLOps platform designed to predict Remaining Useful Life (RUL), identify degradation patterns, explain failure mechanisms, and support proactive maintenance decision-making for industrial hydraulic assets.

The platform transforms raw telemetry sensor data into actionable maintenance intelligence through machine learning, explainable AI, failure pattern recognition, and cloud-based deployment.

Rather than relying solely on failure prediction, the system is designed to help engineers understand:

* How much useful life remains
* Which operational factors are influencing asset health
* How degradation is evolving over time
* Which historical failure patterns the asset most closely resembles
* What maintenance actions may be appropriate

---

## Business Problem

Industrial hydraulic systems are subject to continuous wear caused by thermal stress, vibration exposure, pressure imbalance, equipment ageing, and maintenance delays.

Traditional maintenance approaches often result in:

- Unplanned downtime
- Increased maintenance costs
- Reduced asset availability
- Reactive maintenance practices
- Limited visibility into degradation progression

This project aims to enable condition-based maintenance through predictive analytics and explainable AI.


---


## Solution Overview

The platform consists of five integrated intelligence layers:

### 1. Data Engineering

- Multi-source data ingestion
- Data validation and cleaning
- Temporal alignment
- Asset-level aggregation
- Feature store creation


### 2. Feature Engineering

35 degradation-focused features were engineered across:

- Operational signals
- Maintenance history
- Degradation indicators
- Temporal behaviour patterns

Key engineered features include:

- Cumulative Vibration Exposure
- Thermal Stress Accumulation
- Pressure-Flow Ratio
- Equipment Age
- Maintenance Intervals
- Downtime Exposure


### 3. Remaining Useful Life Prediction

Models evaluated:

- XGBoost
- LightGBM

Final Production Model:

- LightGBM Regressor

Performance:

| Metric | Result |
|----------|----------|
| R² Score | 0.902 |
| MAE | 14.24 Hours |
| Features | 35 |


### 4. Failure Pattern Intelligence

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


### 5. Explainable AI

SHAP explainability provides:

- Feature attribution
- Local prediction explanations
- Maintenance intelligence
- Executive-level transparency

Common degradation drivers:

- Vibration Exposure
- Thermal Stress Accumulation
- Maintenance Delays
- Pressure-Flow Imbalance
- Downtime Exposure

---

### Consistent Degradation Drivers

Across validation samples, the most influential degradation indicators were:

* Thermal stress accumulation
* Vibration accumulation
* Pressure-flow imbalance
* Equipment ageing
* Maintenance delay

These findings align with known industrial asset degradation mechanisms.


## Executive Intelligence Outputs

For every prediction, the system generates:

- Remaining Useful Life (Hours & Days)
- Machine Health Score
- Risk Classification
- Failure Pattern Recognition
- Failure Progression Stage
- SHAP Explainability
- Maintenance Recommendations
- Executive Summary Narrative

---

## Technology Stack

### Development

- Python
- VS Code
- Git

### Data Engineering

- Pandas
- NumPy

### Machine Learning

- LightGBM
- XGBoost
- Scikit-Learn

### Explainable AI

- SHAP

### API Layer

- FastAPI
- Pydantic

### Dashboard

- Streamlit
- Plotly

### MLOps

- MLflow
- DagsHub

### Cloud & Deployment

- Docker
- GitHub Actions
- Amazon S3
- AWS EC2
- AWS ECR

---

## Production Workflow

```text
Sensor Data
    ↓
Feature Engineering
    ↓
LightGBM RUL Prediction
    ↓
Failure Pattern Recognition
    ↓
SHAP Explainability
    ↓
Executive Intelligence
    ↓
Maintenance Recommendations
    ↓
Streamlit Dashboard
```

---

## Project Results

- 126,585 telemetry records processed
- 35 engineered degradation features
- 4 failure modes modelled
- R² Score: 0.902
- MAE: 14.24 Hours
- Production-ready API deployed on AWS
- End-to-end MLOps pipeline implemented
- Explainable AI integrated using SHAP

---

## Project Status

### Completed

- Data Engineering Pipeline
- Feature Engineering Pipeline
- RUL Prediction Engine
- Failure Pattern Intelligence Engine
- SHAP Explainability Layer
- FastAPI Prediction Service
- Streamlit Dashboard
- MLflow Model Registry
- Amazon S3 Integration
- Docker Containerization
- GitHub Actions CI/CD
- AWS Cloud Deployment

--- 

## Author

**Priscillia Eboe-Ogoro**

Data Scientist | Machine Learning Engineer

Interests:

- Explainable AI
- Predictive Maintenance
- Industrial Analytics
- Responsible AI
- Healthcare Data Science
- MLOps & Cloud Engineering

