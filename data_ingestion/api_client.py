import requests
import pandas as pd

BASE_URL = "https://api.co2map.de/intensity"

def get_emission_intensity(state_code: str, date: str) -> pd.DataFrame:
    url = f"{BASE_URL}/{state_code}/{date}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()["data"]
    return pd.DataFrame(data)
