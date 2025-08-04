import sys
from pathlib import Path

import pytest
import requests
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from deployment.api import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_states_endpoint():
    """Test states listing endpoint"""
    response = client.get("/states")
    assert response.status_code == 200
    data = response.json()
    assert "states" in data
    assert "BW" in data["states"]
    assert len(data["states"]) == 13  # 13 German states


def test_prediction_endpoint():
    """Test prediction endpoint"""
    payload = {
        "state": "BW",
        "intensity_type": "consumption",
        "hour": 12,
        "day_of_week": 0,
        "month": 8,
        "quarter": 3,
        "is_weekend": False,
        "value_lag_1": 150.0,
        "value_lag_2": 148.0,
        "value_lag_3": 145.0,
        "value_lag_24": 140.0,
        "value_lag_48": 135.0,
        "value_lag_168": 142.0,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "unit" in data
    assert "state" in data
    assert "timestamp" in data

    assert data["unit"] == "gCO₂/kWh"
    assert data["state"] == "BW"
    assert isinstance(data["prediction"], float)


def test_prediction_invalid_state():
    """Test prediction with invalid state"""
    payload = {"state": "INVALID", "intensity_type": "consumption", "hour": 12}

    response = client.post("/predict", json=payload)
    assert response.status_code == 400


def test_prediction_invalid_hour():
    """Test prediction with invalid hour"""
    payload = {
        "state": "BW",
        "intensity_type": "consumption",
        "hour": 25,  # Invalid hour
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 400
