import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from data_processing.prepare_features import create_time_features, create_lag_features

def test_create_time_features():
    """Test time feature creation"""
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(['2022-01-01 12:00:00', '2022-01-02 18:30:00']),
        'value': [100, 200]
    })
    
    result = create_time_features(df)
    
    assert 'hour' in result.columns
    assert 'day_of_week' in result.columns
    assert 'month' in result.columns
    assert 'quarter' in result.columns
    assert 'is_weekend' in result.columns
    
    assert result['hour'].iloc[0] == 12
    assert result['hour'].iloc[1] == 18
    assert result['month'].iloc[0] == 1

def test_create_lag_features():
    """Test lag feature creation"""
    df = pd.DataFrame({
        'timestamp': pd.date_range('2022-01-01', periods=10, freq='H'),
        'value': range(10),
        'state': ['BW'] * 10,
        'type': ['consumption'] * 10
    })
    
    result = create_lag_features(df, lags=[1, 2])
    
    assert 'value_lag_1' in result.columns
    assert 'value_lag_2' in result.columns
    
    # Check lag values
    assert pd.isna(result['value_lag_1'].iloc[0])  # First row should be NaN
    assert result['value_lag_1'].iloc[1] == 0      # Second row should be first value

def test_data_processing_pipeline():
    """Integration test for data processing"""
    # This would normally use real data, but we'll create mock data
    df = pd.DataFrame({
        'timestamp': pd.date_range('2022-01-01', periods=200, freq='H'),
        'value': np.random.normal(150, 20, 200),
        'state': ['BW'] * 200,
        'type': ['consumption'] * 200
    })
    
    # Process data
    df = create_time_features(df)
    df = create_lag_features(df, lags=[1, 24])
    df = df.dropna()
    
    # Check final dataset
    expected_cols = ['timestamp', 'value', 'state', 'type', 'hour', 'day_of_week', 
                     'month', 'quarter', 'is_weekend', 'value_lag_1', 'value_lag_24']
    
    for col in expected_cols:
        assert col in df.columns
    
    assert len(df) > 0
    assert not df.isnull().any().any()  # No NaN values should remain
