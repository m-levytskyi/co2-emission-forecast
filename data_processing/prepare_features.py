import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from data_ingestion.config import DATA_DIR, STATE_CODES


def load_and_combine_data(states=None):
    """Load and combine consumption/production data from multiple states"""
    if states is None:
        states = STATE_CODES

    all_data = []

    for state in states:
        consumption_file = DATA_DIR / f"{state}_consumption_intensity.csv"
        production_file = DATA_DIR / f"{state}_production_intensity.csv"

        if consumption_file.exists():
            df_cons = pd.read_csv(consumption_file)
            # Handle legacy format
            if list(df_cons.columns) == ["0", "1"]:
                df_cons.columns = ["timestamp", "value"]
            df_cons["state"] = state
            df_cons["type"] = "consumption"
            all_data.append(df_cons)

        if production_file.exists():
            df_prod = pd.read_csv(production_file)
            if list(df_prod.columns) == ["0", "1"]:
                df_prod.columns = ["timestamp", "value"]
            df_prod["state"] = state
            df_prod["type"] = "production"
            all_data.append(df_prod)

    combined = pd.concat(all_data, ignore_index=True)
    combined["timestamp"] = pd.to_datetime(combined["timestamp"])
    return combined


def create_time_features(df):
    """Create time-based features for ML"""
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["month"] = df["timestamp"].dt.month
    df["quarter"] = df["timestamp"].dt.quarter
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    return df


def create_lag_features(df, target_col="value", lags=[1, 2, 3, 24, 48, 168]):
    """Create lagged features for time series"""
    df = df.copy()
    df = df.sort_values(["state", "type", "timestamp"])

    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df.groupby(["state", "type"])[target_col].shift(
            lag
        )

    return df


def prepare_ml_dataset(output_path="data/processed/ml_dataset.csv"):
    """Main pipeline to prepare ML-ready dataset"""
    print("Loading raw data...")
    df = load_and_combine_data()

    print("Creating time features...")
    df = create_time_features(df)

    print("Creating lag features...")
    df = create_lag_features(df)

    # Remove rows with NaN values from lag features
    df = df.dropna()

    # Create output directory
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"Dataset shape: {df.shape}")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/processed/ml_dataset.csv")
    args = parser.parse_args()

    prepare_ml_dataset(args.output)
