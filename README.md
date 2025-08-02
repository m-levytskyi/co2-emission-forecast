# CO₂ Emission Forecast

This repository is part of the MLOps Zoomcamp 2025. It focuses on collecting, preprocessing, and forecasting CO₂ emissions using publicly available data from German electricity consumption and production.

## Structure

```
co2-emission-forecast/
│
├── data_ingestion/
│   ├── fetch_intensity.py        # Downloads CO₂ intensity and consumption data
│   ├── utils.py                  # Helper functions for data loading and date logic
│
├── data/
│   ├── raw/                      # Downloaded raw data in CSV format
│   └── processed/                # Cleaned and transformed data for modeling
│
├── notebooks/
│   ├── exploration.ipynb         # Initial data exploration and visualization
│
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Usage

### Download data

```bash
python data_ingestion/fetch_intensity.py \
  --start 2022-01-01 \
  --end 2022-12-31 \
  --region BW
```

- The script fetches and stores CO₂ intensity and consumption data for the specified date range and region.
- Supports incremental fetching without overwriting existing data.
- Skips malformed rows automatically.

### Data source

Data is sourced from the *Open Data Platform of the German TSOs* (transnetbw, 50Hertz, etc.). Endpoints are specific to each region (e.g. BW for Baden-Württemberg).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Requirements

- Python 3.10+
- Pandas
- Requests
- Typer

## License

MIT