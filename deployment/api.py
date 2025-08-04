from datetime import datetime
from typing import Optional

import mlflow
import mlflow.xgboost
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="CO₂ Intensity Forecast API",
    description="Predict German electricity CO₂ intensity using XGBoost",
    version="1.0.0",
)

# Global model variable
model = None


class PredictionRequest(BaseModel):
    state: str = "BW"  # German state code
    intensity_type: str = "consumption"  # consumption or production
    hour: int = 12
    day_of_week: int = 0  # 0=Monday, 6=Sunday
    month: int = 8
    quarter: int = 3
    is_weekend: bool = False
    value_lag_1: float = 150.0
    value_lag_2: float = 148.0
    value_lag_3: float = 145.0
    value_lag_24: float = 140.0
    value_lag_48: float = 135.0
    value_lag_168: float = 142.0


class PredictionResponse(BaseModel):
    prediction: float
    unit: str = "gCO₂/kWh"
    state: str
    intensity_type: str
    timestamp: str


@app.on_event("startup")
async def load_model():
    """Load model from MLflow registry on startup"""
    global model
    try:
        model_uri = "models:/co2-intensity-xgboost/latest"
        model = mlflow.xgboost.load_model(model_uri)
        print("Model loaded successfully from MLflow registry")
    except Exception as e:
        print(f"Failed to load model: {e}")
        # Fallback: try loading from local mlruns
        try:
            import os

            runs_dir = "mlruns/1"  # Experiment 1
            if os.path.exists(runs_dir):
                run_dirs = [
                    d
                    for d in os.listdir(runs_dir)
                    if os.path.isdir(os.path.join(runs_dir, d))
                ]
                if run_dirs:
                    latest_run = sorted(run_dirs)[-1]
                    model_path = f"mlruns/1/{latest_run}/artifacts/model"
                    model = mlflow.xgboost.load_model(model_path)
                    print("Model loaded from local mlruns")
        except Exception as fallback_e:
            print(f"Fallback load failed: {fallback_e}")


# State and type encoding mappings (from training)
STATE_ENCODING = {
    "BW": 0,
    "BY": 1,
    "BB": 2,
    "HE": 3,
    "MV": 4,
    "NI": 5,
    "NW": 6,
    "RP": 7,
    "SL": 8,
    "SN": 9,
    "ST": 10,
    "SH": 11,
    "TH": 12,
}
TYPE_ENCODING = {"consumption": 0, "production": 1}


@app.get("/")
async def root():
    return {"message": "CO₂ Intensity Forecast API", "status": "running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make CO₂ intensity prediction"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate inputs
    if request.state not in STATE_ENCODING:
        raise HTTPException(status_code=400, detail=f"Invalid state: {request.state}")
    if request.intensity_type not in TYPE_ENCODING:
        raise HTTPException(
            status_code=400, detail=f"Invalid type: {request.intensity_type}"
        )
    if not (0 <= request.hour <= 23):
        raise HTTPException(status_code=400, detail="Hour must be 0-23")

    # Prepare features in training order
    features = pd.DataFrame(
        {
            "hour": [request.hour],
            "day_of_week": [request.day_of_week],
            "month": [request.month],
            "quarter": [request.quarter],
            "is_weekend": [int(request.is_weekend)],
            "value_lag_1": [request.value_lag_1],
            "value_lag_2": [request.value_lag_2],
            "value_lag_3": [request.value_lag_3],
            "value_lag_24": [request.value_lag_24],
            "value_lag_48": [request.value_lag_48],
            "value_lag_168": [request.value_lag_168],
            "state_encoded": [STATE_ENCODING[request.state]],
            "type_encoded": [TYPE_ENCODING[request.intensity_type]],
        }
    )

    # Make prediction
    prediction = model.predict(features)[0]

    return PredictionResponse(
        prediction=float(prediction),
        state=request.state,
        intensity_type=request.intensity_type,
        timestamp=datetime.now().isoformat(),
    )


@app.get("/states")
async def get_states():
    """Get available German states"""
    return {"states": list(STATE_ENCODING.keys())}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
