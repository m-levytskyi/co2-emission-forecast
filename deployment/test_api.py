import requests
import json

# Test the API
BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health: {response.json()}")

def test_prediction():
    payload = {
        "state": "BW",
        "intensity_type": "consumption", 
        "hour": 14,
        "day_of_week": 0,
        "month": 8,
        "quarter": 3,
        "is_weekend": False,
        "value_lag_1": 155.0,
        "value_lag_2": 152.0,
        "value_lag_3": 148.0,
        "value_lag_24": 145.0,
        "value_lag_48": 142.0,
        "value_lag_168": 150.0
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Prediction: {response.json()}")

def test_states():
    response = requests.get(f"{BASE_URL}/states")
    print(f"States: {response.json()}")

if __name__ == "__main__":
    test_health()
    test_states()
    test_prediction()
