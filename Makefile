# CO₂ Emission Forecast MLOps Pipeline

.PHONY: install prepare-data train-model help

install:
	pipenv install

prepare-data:
	pipenv run python data_processing/prepare_features.py

train-model:
	pipenv run python experiments/train_model.py

train-cv:
	pipenv run python experiments/train_model.py --mode cv

predict:
	pipenv run python experiments/predict.py

# Deployment targets
serve:
	pipenv run uvicorn deployment.api:app --host 0.0.0.0 --port 8000 --reload

test-api:
	pipenv run python deployment/test_api.py

docker-build:
	docker build -t co2-forecast-api .

docker-run:
	docker run -p 8000:8000 co2-forecast-api

docker-compose-up:
	docker-compose up -d

# Testing targets
test:
	pipenv run pytest tests/ -v

test-unit:
	pipenv run pytest tests/test_data_processing.py -v

test-integration:
	pipenv run pytest tests/test_api.py -v

# Monitoring targets
monitor:
	pipenv run python monitoring/monitor.py

# Workflow orchestration
pipeline:
	pipenv run python infra/pipeline.py

docker-compose-down:
	docker-compose down

mlflow-ui:
	pipenv run mlflow ui

help:
	@echo "Available commands:"
	@echo "  install           - Install dependencies with pipenv"
	@echo "  prepare-data      - Process raw data into ML-ready format"
	@echo "  train-model       - Train XGBoost model with MLflow tracking"
	@echo "  train-cv          - Run cross-validation"
	@echo "  predict           - Test model predictions from registry"
	@echo "  serve             - Start FastAPI development server"
	@echo "  test-api          - Test API endpoints"
	@echo "  test              - Run all tests"
	@echo "  test-unit         - Run unit tests"
	@echo "  test-integration  - Run integration tests"
	@echo "  monitor           - Run monitoring checks"
	@echo "  pipeline          - Run full MLOps pipeline"
	@echo "  docker-build      - Build Docker image"
	@echo "  docker-run        - Run Docker container"
	@echo "  docker-compose-up - Start services with docker-compose"
	@echo "  mlflow-ui         - Start MLflow UI server"