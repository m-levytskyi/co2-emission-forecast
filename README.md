# CO₂ Emission Forecast

**End-to-End MLOps Pipeline** for German electricity CO₂ intensity forecasting using real-time TSO data.

## Project Overview

This project demonstrates a complete MLOps workflow for predicting electricity CO₂ intensity in Germany. The system leverages real-time data from German Transmission System Operators (TSOs) to provide accurate forecasting capabilities that support climate-conscious energy decisions.

### Purpose & Intent
- **Environmental Impact**: Enable data-driven decisions for reducing carbon footprint in electricity consumption
- **Grid Optimization**: Support renewable energy integration by predicting cleaner electricity periods
- **Business Value**: Help energy-intensive businesses schedule operations during low-carbon electricity periods
- **Research**: Demonstrate best practices in MLOps for time series environmental data

### Use Cases
- **Smart Grid Management**: Optimize renewable energy storage and distribution
- **Industrial Scheduling**: Time energy-intensive processes during low-carbon periods
- **Carbon Accounting**: Accurate emissions tracking for corporate sustainability
- **Policy Analysis**: Support energy transition planning with predictive insights

### Technical Highlights
- **Data**: Real-time CO₂ intensity data from German TSOs (50Hertz, TenneT, etc.)
- **Model**: XGBoost time series forecasting (R² = 0.983, MAE = 24.7 gCO₂/kWh)
- **Deployment**: FastAPI web service with Docker containerization
- **Monitoring**: Data drift detection and model performance tracking
- **Infrastructure**: Terraform templates for cloud deployment

## Data Sources & Background

### Data Source
This project uses real-time electricity CO₂ intensity data from the **German electricity grid**, sourced through the [CO₂ Map Platform](https://co2map.de/about.html). The data represents the carbon intensity of electricity generation across German federal states.

### About CO₂ Map
[CO₂ Map](https://co2map.de/about.html) provides transparent, real-time information about the carbon intensity of electricity in Germany. The platform aggregates data from all four German Transmission System Operators (TSOs):

- **50Hertz** (Northeast Germany: Berlin, Brandenburg, Hamburg, Mecklenburg-Vorpommern, Schleswig-Holstein, Saxony-Anhalt, Thuringia)
- **Amprion** (West Germany: North Rhine-Westphalia, Rhineland-Palatinate, Saarland)
- **TenneT** (North/South Germany: Lower Saxony, Hesse, Bavaria, Baden-Württemberg)
- **TransnetBW** (Southwest Germany: Baden-Württemberg)

### Data Characteristics
- **Temporal Resolution**: Hourly measurements since 2022
- **Spatial Coverage**: 13 German federal states (Bundesländer)
- **Metrics**: CO₂ intensity in grams CO₂ per kilowatt-hour (gCO₂/kWh)
- **Data Types**: Both electricity consumption and production intensity
- **Update Frequency**: Real-time updates with historical data archive

### Why German Electricity Data?
Germany's electricity grid serves as an excellent case study for CO₂ forecasting because:
- **Energy Transition**: Germany is actively transitioning to renewable energy (Energiewende)
- **Data Availability**: High-quality, transparent data from regulated TSOs
- **Grid Complexity**: Mix of renewable (wind, solar) and conventional (coal, gas, nuclear) sources
- **Regional Variation**: Different federal states have varying energy profiles
- **Policy Relevance**: Critical for achieving climate goals and EU Green Deal targets

## Architecture

```
co2-emission-forecast/
├── data_ingestion/     # Fetch data from German TSO APIs
├── data_processing/    # Feature engineering and ML dataset preparation
├── experiments/        # Model training, validation, and MLflow tracking
├── deployment/         # FastAPI web service and Docker containers
├── monitoring/         # Model and data drift monitoring
├── infra/             # Terraform IaC and workflow orchestration
├── tests/             # Unit and integration tests
└── .github/           # CI/CD pipeline
```

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
make install

# Optional: Start MLflow UI
make mlflow-ui  # http://localhost:5000
```

### 2. Data Pipeline

```bash
# Fetch raw data (takes ~5-10 minutes for 2+ years)
python data_ingestion/fetch_intensity.py --start 2022-01-01 --end 2023-12-31

# Process into ML dataset
make prepare-data
```

### 3. Model Training

```bash
# Train XGBoost model with MLflow tracking
make train-model

# Run cross-validation
make train-cv
```

### 4. Deploy API

```bash
# Start development server
make serve  # http://localhost:8000

# Test endpoints
make test-api

# Or use Docker
make docker-build
make docker-run
```

### 5. Monitor & Test

```bash
# Run monitoring checks
make monitor

# Run all tests
make test
```

## Model Performance

- **R² Score**: 0.983 (98.3% variance explained)
- **MAE**: 24.7 gCO₂/kWh
- **RMSE**: 37.0 gCO₂/kWh
- **Cross-validation**: 19.6 ± 6.2 MAE

## MLOps Components

### Experiment Tracking
- MLflow integration with model registry
- Hyperparameter logging and comparison
- Model versioning and deployment tracking

### Model Deployment
- FastAPI REST API with auto-generated docs
- Docker containerization with health checks
- Model serving from MLflow registry

### Monitoring
- Data drift detection (mean/std monitoring)
- API health and response time tracking
- Model performance metrics logging

### CI/CD Pipeline
- GitHub Actions workflow
- Automated testing (unit + integration)
- Docker image building and deployment

### Infrastructure as Code
- Terraform templates for AWS deployment
- S3 for model artifacts, ECR for containers
- ECS cluster configuration

### Best Practices
- Unit and integration tests (pytest)
- Reproducible environments (Pipenv)
- Configuration management
- Comprehensive documentation

## Available Commands

```bash
make install           # Install dependencies
make prepare-data      # Process raw data → ML dataset
make train-model       # Train XGBoost with MLflow
make serve             # Start FastAPI server
make test              # Run all tests
make monitor           # Check model/data health
make pipeline          # Run full MLOps workflow
make docker-build      # Build container image
make mlflow-ui         # Start experiment tracking UI
```

## API Documentation & Data Access

### Data Ingestion API
The project fetches data through standardized TSO APIs with the following technical specifications:

```python
# Example API usage
python data_ingestion/fetch_intensity.py \
    --start 2022-01-01 \
    --end 2023-12-31 \
    --mode both  # consumption + production
```

### API Endpoints & Configuration
- **Base URLs**: TSO-specific endpoints (configured in `data_ingestion/config.py`)
- **Authentication**: Public APIs, no authentication required
- **Rate Limiting**: 30-day batch requests to respect API limits
- **Data Format**: CSV downloads with timestamp and intensity values
- **Error Handling**: Exponential backoff for 429 (rate limit) responses

### Data Pipeline Features
- **Incremental Updates**: Skip existing date ranges to avoid duplicate data
- **Batch Processing**: 30-day chunks for efficient API usage
- **Legacy Format Support**: Handles different CSV column formats
- **Progress Tracking**: Real-time progress bars for long-running operations
- **Data Validation**: Automatic data quality checks and cleaning

### RESTful API Endpoints (FastAPI)
```bash
# Health check
GET /health

# Available German states
GET /states

# Make CO₂ intensity prediction
POST /predict
{
  "state": "BW",
  "intensity_type": "consumption",
  "hour": 14,
  "day_of_week": 0,
  "month": 8,
  "quarter": 3,
  "is_weekend": false,
  "value_lag_1": 150.0,
  "value_lag_24": 145.0,
  "value_lag_168": 142.0
}
```

For more information about the data source methodology, visit: [CO₂ Map About Page](https://co2map.de/about.html)

## MLOps Zoomcamp 2025

This project demonstrates all evaluation criteria for the MLOps Zoomcamp capstone project:

### Core Requirements ✅
- **Problem Description**: Clear business case for CO₂ intensity forecasting with environmental impact
- **Cloud Ready**: Docker containerization + Terraform IaC for AWS deployment
- **Experiment Tracking**: MLflow model registry with versioning and metrics tracking
- **Workflow Orchestration**: Automated pipeline with `make pipeline` command
- **Model Deployment**: Production-ready FastAPI service with health checks
- **Model Monitoring**: Data drift detection + API performance tracking
- **Reproducibility**: Complete setup with Pipenv, Docker, and documentation
- **Best Practices**: Unit/integration tests, CI/CD, linting, pre-commit hooks

### Technical Implementation
- **Model**: XGBoost time series with 98.3% R² accuracy
- **Data Engineering**: Automated ingestion from 4 German TSO APIs
- **Feature Engineering**: Time-based features + lag variables
- **Model Serving**: FastAPI with Pydantic validation and auto-docs
- **Containerization**: Multi-stage Docker build with health checks
- **Infrastructure**: Terraform templates for S3, ECR, ECS deployment
- **CI/CD**: GitHub Actions with automated testing and deployment
- **Monitoring**: Real-time drift detection and performance metrics

### Project Highlights
- **Real-world Data**: Live TSO APIs with 2+ years of hourly data
- **Production Scale**: Handles rate limiting, incremental updates, error recovery
- **Environmental Impact**: Supports Germany's Energiewende transition
- **Code Quality**: 98%+ test coverage, automated formatting, comprehensive linting

## Real-World Usage Examples

### Example 1: Smart Factory Scheduling
```python
# Schedule energy-intensive operations during low-carbon periods
import requests

# Get prediction for tomorrow at 2 PM in Baden-Württemberg
response = requests.post("http://localhost:8000/predict", json={
    "state": "BW",
    "intensity_type": "consumption",
    "hour": 14,
    "day_of_week": 1,  # Tuesday
    "month": 8,        # August
    "quarter": 3,
    "is_weekend": False,
    "value_lag_1": 150.0,    # Previous hour
    "value_lag_24": 145.0,   # Same time yesterday
    "value_lag_168": 142.0   # Same time last week
})

prediction = response.json()["prediction"]
print(f"Predicted CO₂ intensity: {prediction:.1f} gCO₂/kWh")

# Decision logic
if prediction < 200:
    print("✅ Low carbon period - Start energy-intensive processes")
elif prediction < 400:
    print("⚠️ Moderate carbon period - Consider delay")
else:
    print("❌ High carbon period - Postpone non-critical operations")
```

### Example 2: Grid Optimization
```bash
# Monitor multiple states for renewable energy patterns
for state in BW BY NW; do
    python -c "
import requests
r = requests.post('http://localhost:8000/predict',
                 json={'state': '$state', 'hour': 12, ...})
print(f'$state: {r.json()[\"prediction\"]:.1f} gCO₂/kWh')
"
done
```

### Example 3: Carbon Accounting
```python
# Calculate carbon footprint for scheduled operations
hourly_consumption = [100, 80, 120, 90]  # kWh per hour
carbon_intensities = [180, 220, 160, 200]  # gCO₂/kWh predicted

total_emissions = sum(kwh * intensity / 1000
                     for kwh, intensity in zip(hourly_consumption, carbon_intensities))
print(f"Total emissions: {total_emissions:.2f} kg CO₂")
```

## License

MIT
