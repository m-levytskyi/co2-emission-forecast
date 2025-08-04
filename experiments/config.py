# Experiments configuration
EXPERIMENT_NAME = "co2-intensity-forecast"
MODEL_NAME = "co2-intensity-xgboost"

# Model parameters
XGBOOST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}

# Feature engineering
LAG_FEATURES = [1, 2, 3, 24, 48, 168]  # Hours
TEST_SIZE = 0.2
CV_SPLITS = 5

# MLflow settings
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
