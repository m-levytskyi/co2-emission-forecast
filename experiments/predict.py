import mlflow
import mlflow.xgboost
import pandas as pd
import numpy as np
from pathlib import Path

def load_model_from_registry(model_name="co2-intensity-xgboost", version="latest"):
    """Load model from MLflow model registry"""
    model_uri = f"models:/{model_name}/{version}"
    model = mlflow.xgboost.load_model(model_uri)
    return model

def predict_sample(model, state="BW", intensity_type="consumption", hour=12):
    """Make a sample prediction"""
    # Create sample features in the correct order from training
    sample_data = pd.DataFrame({
        'hour': [hour],
        'day_of_week': [0],    # Monday
        'month': [8],          # August
        'quarter': [3],        # Q3
        'is_weekend': [0],     # Weekday
        'value_lag_1': [150.0],
        'value_lag_2': [148.0],
        'value_lag_3': [145.0],
        'value_lag_24': [140.0],
        'value_lag_48': [135.0],
        'value_lag_168': [142.0],
        'state_encoded': [0],  # BW encoded as 0
        'type_encoded': [0],   # consumption encoded as 0
    })
    
    prediction = model.predict(sample_data)
    return prediction[0]

def main():
    print("Loading model from registry...")
    model = load_model_from_registry()
    
    print("Making sample predictions...")
    for hour in [6, 12, 18, 22]:
        pred = predict_sample(model, hour=hour)
        print(f"Hour {hour:2d}: {pred:.1f} gCO₂/kWh")

if __name__ == "__main__":
    main()
