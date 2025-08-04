# CO₂ Emission Forecast

**End-to-End MLOps Pipeline** for German electricity CO₂ intensity forecasting using real-time TSO data.

## Project Overview

This project demonstrates a complete MLOps workflow from data ingestion to model deployment and monitoring:

- **Data**: Real-time CO₂ intensity data from German TSOs (50Hertz, TenneT, etc.)
- **Model**: XGBoost time series forecasting (R² = 0.983, MAE = 24.7 gCO₂/kWh)
- **Deployment**: FastAPI web service with Docker containerization
- **Monitoring**: Data drift detection and model performance tracking
- **Infrastructure**: Terraform templates for cloud deployment

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

## Data Sources

Data sourced from **Open Data Platform of German TSOs**:
- 50Hertz, Amprion, TenneT, TransnetBW
- Real-time CO₂ intensity (gCO₂/kWh)
- 13 German federal states
- Hourly resolution since 2022

## MLOps Zoomcamp 2025

This project covers all evaluation criteria:
- Problem Description: Clear forecasting objective  
- Cloud Ready: Docker + Terraform for deployment
- Experiment Tracking: MLflow model registry
- Workflow Orchestration: Automated pipeline
- Model Deployment: Containerized FastAPI service
- Model Monitoring: Drift detection + alerting
- Reproducibility: Complete setup instructions
- Best Practices: Tests, CI/CD, IaC, linting

## License

MIT