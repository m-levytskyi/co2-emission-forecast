import pandas as pd
import numpy as np
from pathlib import Path
import mlflow
import mlflow.tracking
from datetime import datetime, timedelta
import requests
import json

def calculate_model_metrics(y_true, y_pred):
    """Calculate monitoring metrics"""
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'timestamp': datetime.now().isoformat()
    }

def monitor_data_drift(current_data, reference_data):
    """Simple data drift monitoring"""
    current_mean = current_data.mean()
    reference_mean = reference_data.mean()
    current_std = current_data.std()
    reference_std = reference_data.std()
    
    mean_drift = abs(current_mean - reference_mean) / reference_std
    std_drift = abs(current_std - reference_std) / reference_std
    
    return {
        'mean_drift': mean_drift,
        'std_drift': std_drift,
        'drift_detected': mean_drift > 2.0 or std_drift > 0.5,
        'timestamp': datetime.now().isoformat()
    }

def test_api_health():
    """Monitor API health and response time"""
    start_time = datetime.now()
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'response_time_seconds': response_time,
            'status_code': response.status_code,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def log_monitoring_metrics(metrics):
    """Log monitoring metrics to MLflow"""
    with mlflow.start_run():
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)
        
        mlflow.log_params({
            'monitoring_type': 'model_performance',
            'timestamp': datetime.now().isoformat()
        })

def generate_monitoring_report():
    """Generate a simple monitoring report"""
    print("CO₂ Forecast Model Monitoring Report")
    print("=" * 50)
    
    # Test API health
    health = test_api_health()
    print(f"API Status: {health['status']}")
    if 'response_time_seconds' in health:
        print(f"Response Time: {health['response_time_seconds']:.3f}s")
    
    # Load recent data for drift monitoring
    try:
        df = pd.read_csv("data/processed/ml_dataset.csv")
        recent_data = df['value'].tail(1000)  # Last 1000 records
        reference_data = df['value'].head(1000)  # First 1000 records
        
        drift_metrics = monitor_data_drift(recent_data, reference_data)
        print(f"Data Drift Detected: {drift_metrics['drift_detected']}")
        print(f"Mean Drift: {drift_metrics['mean_drift']:.3f}")
        print(f"Std Drift: {drift_metrics['std_drift']:.3f}")
        
    except Exception as e:
        print(f"Data drift monitoring failed: {e}")
    
    print("=" * 50)
    print(f"Report generated at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    generate_monitoring_report()
