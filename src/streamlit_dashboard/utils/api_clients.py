import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000"
)

print("=" * 50)
print("API URL:", BASE_URL)
print("=" * 50)


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
    except Exception as e:
        print("API HEALTH CHECK FAILED:", e)
        return False

def retrain_model() -> dict:
    response = requests.post(
        f"{BASE_URL}/train",
        timeout=600
    )
    response.raise_for_status()
    return response.json()
