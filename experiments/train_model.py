import pandas as pd
import numpy as np
from pathlib import Path
import mlflow
import mlflow.xgboost
import mlflow.sklearn
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import argparse
from datetime import datetime

# Set MLflow experiment
mlflow.set_experiment("co2-intensity-forecast")

def load_processed_data(data_path="data/processed/ml_dataset.csv"):
    """Load preprocessed ML dataset"""
    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def prepare_features(df):
    """Prepare features for training"""
    # Encode categorical variables
    le_state = LabelEncoder()
    le_type = LabelEncoder()
    
    df['state_encoded'] = le_state.fit_transform(df['state'])
    df['type_encoded'] = le_type.fit_transform(df['type'])
    
    # Feature columns (exclude target and identifiers)
    feature_cols = [col for col in df.columns if col not in 
                   ['timestamp', 'value', 'state', 'type']]
    
    X = df[feature_cols]
    y = df['value']
    
    return X, y, le_state, le_type

def train_xgboost_model(X, y, test_size=0.2, random_state=42):
    """Train XGBoost model with MLflow tracking"""
    
    with mlflow.start_run():
        # Split data (time-aware split for time series)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=False
        )
        
        # Model parameters
        params = {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': random_state
        }
        
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))
        
        # Train model
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate metrics
        train_mae = mean_absolute_error(y_train, y_pred_train)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        train_r2 = r2_score(y_train, y_pred_train)
        
        test_mae = mean_absolute_error(y_test, y_pred_test)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        test_r2 = r2_score(y_test, y_pred_test)
        
        # Log metrics
        mlflow.log_metrics({
            "train_mae": train_mae,
            "train_rmse": train_rmse,
            "train_r2": train_r2,
            "test_mae": test_mae,
            "test_rmse": test_rmse,
            "test_r2": test_r2
        })
        
        # Log model
        mlflow.xgboost.log_model(
            model, 
            "model",
            registered_model_name="co2-intensity-xgboost"
        )
        
        print(f"Model trained and logged to MLflow")
        print(f"Test MAE: {test_mae:.3f}")
        print(f"Test RMSE: {test_rmse:.3f}")
        print(f"Test R²: {test_r2:.3f}")
        
        return model, {
            'test_mae': test_mae,
            'test_rmse': test_rmse,
            'test_r2': test_r2
        }

def cross_validate_model(X, y, n_splits=5):
    """Perform time series cross-validation"""
    
    with mlflow.start_run():
        tscv = TimeSeriesSplit(n_splits=n_splits)
        
        cv_scores = []
        
        for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
            X_train_fold = X.iloc[train_idx]
            X_val_fold = X.iloc[val_idx]
            y_train_fold = y.iloc[train_idx]
            y_val_fold = y.iloc[val_idx]
            
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            model.fit(X_train_fold, y_train_fold)
            y_pred_fold = model.predict(X_val_fold)
            
            fold_mae = mean_absolute_error(y_val_fold, y_pred_fold)
            cv_scores.append(fold_mae)
            
            mlflow.log_metric(f"fold_{fold}_mae", fold_mae)
        
        cv_mean = np.mean(cv_scores)
        cv_std = np.std(cv_scores)
        
        mlflow.log_metrics({
            "cv_mean_mae": cv_mean,
            "cv_std_mae": cv_std
        })
        
        print(f"Cross-validation MAE: {cv_mean:.3f} ± {cv_std:.3f}")
        
        return cv_scores

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/processed/ml_dataset.csv")
    parser.add_argument("--mode", choices=["train", "cv"], default="train")
    args = parser.parse_args()
    
    print("Loading data...")
    df = load_processed_data(args.data)
    
    print("Preparing features...")
    X, y, le_state, le_type = prepare_features(df)
    
    if args.mode == "train":
        print("Training model...")
        model, metrics = train_xgboost_model(X, y)
    elif args.mode == "cv":
        print("Running cross-validation...")
        cv_scores = cross_validate_model(X, y)

if __name__ == "__main__":
    main()
