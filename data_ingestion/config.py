from pathlib import Path

BASE_URL = "https://api.co2map.de/"
CONSUMPTION_INTENSITY = "ConsumptionIntensityHistorical/"
PRODUCTION_INTENSITY = "ProductionIntensityHistorical/"

STATE_CODES = [
    "BW", "BY", "BE", "BB", "HB", "HH", "HE", "MV",
    "NI", "NW", "RP", "SL", "SN", "ST", "SH", "TH"
]

DEFAULT_START_DATE = "2022-01-01"
DEFAULT_END_DATE = "2025-07-27"

BATCH_DAYS = 30
DATA_DIR = Path("data/raw")