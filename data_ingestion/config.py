from pathlib import Path

BASE_URL = "https://api.co2map.de/"
CONSUMPTION_INTENSITY = "ConsumptionIntensityHistorical/"
PRODUCTION_INTENSITY = "ProductionIntensityHistorical/"

STATE_CODES = [
    "BW",  # Baden-Wuerttemberg
    "BY",  # Bavaria
    "BB",  # Brandenburg and Berlin
    "HE",  # Hesse
    "MV",  # Mecklenburg-Western Pomerania
    "NI",  # Lower Saxony and Bremen
    "NW",  # North Rhine-Westphalia
    "RP",  # Rhineland-Palatinate
    "SL",  # Saarland
    "SN",  # Saxony
    "ST",  # Saxony-Anhalt
    "SH",  # Schleswig-Holstein and Hamburg
    "TH",  # Thuringia
]

DEFAULT_START_DATE = "2022-01-01"
DEFAULT_END_DATE = "2025-07-27"

BATCH_DAYS = 30
DATA_DIR = Path("data/raw")
