import requests


#BASE_URL = "http://localhost:8000"

BASE_URL = "http://3.87.72.44:8000"

def predict_asset(payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/predict",
        json=payload,
        timeout=90
    )
    response.raise_for_status()
    return response.json()


def check_api_health() -> bool:
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        return False


def retrain_model() -> dict:
    response = requests.post(
        f"{BASE_URL}/train",
        timeout=600
    )
    response.raise_for_status()
    return response.json()



