# CO₂ Emission Forecast - AI Coding Instructions

## General Coding Philosophy
- Write **MINIMUM CODE** required - prioritize simple, elegant solutions over defensive programming
- NO exception handling unless absolutely essential to requirements
- NO emojis, avoid overengineering and unnecessary abstractions
- Follow task instructions strictly - don't add unrequested features
- Leverage built-in language/library features over custom implementations

## Project Architecture

### Data Flow
This is an MLOps project for German electricity CO₂ intensity forecasting:
1. **Data Ingestion** (`data_ingestion/`) - Fetches timestamped CO₂ data from German TSO APIs
2. **Data Processing** (`data_processing/`) - Transform raw CSV files for ML training
3. **Experiments** (`experiments/`) - Model training and tracking
4. **Deployment** (`deployment/`) - Model serving infrastructure  
5. **Monitoring** (`monitoring/`) - Model performance tracking

### Key Patterns

**Configuration Management**: All constants in `data_ingestion/config.py`
- API endpoints, state codes, date ranges, batch sizes
- Use `STATE_CODES` for German federal states (BW, BY, BB, etc.)

**Data Storage Convention**: 
- Raw data: `data/raw/{STATE}_{consumption|production}_intensity.csv`
- Format: `[timestamp, value]` columns only
- DVC tracks `data/raw/` directory (see `data/raw.dvc`)

**Rate-Limited API Pattern** (`fetch_intensity.py`):
- Batch requests by `BATCH_DAYS` (30-day chunks)
- Exponential backoff on 429 errors
- Incremental fetching - skip existing date ranges
- Legacy CSV format handling in `load_existing_csv()`

**Entry Points**:
```bash
# Data fetching
python data_ingestion/fetch_intensity.py --start 2022-01-01 --end 2023-12-31 --mode both

# Environment setup
pipenv install  # Python 3.10 + deps in Pipfile
```

### Development Workflow
- **Package Manager**: Pipenv (not pip/conda)
- **Data Versioning**: DVC for `data/raw/` directory
- **Project Structure**: Modular MLOps pipeline (ingest → process → experiment → deploy → monitor)
- **File Naming**: Snake_case for Python files, state prefixes for data files

When implementing new components, follow the established patterns:
- Put configuration in dedicated config files
- Use pandas for data manipulation with standardized timestamp handling
- Implement incremental processing to avoid duplicate work
- Use tqdm for progress bars on long-running operations