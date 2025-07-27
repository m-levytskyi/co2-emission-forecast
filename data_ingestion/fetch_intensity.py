import requests
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import time
from pathlib import Path

from config import START_DATE, END_DATE, STATE, BATCH_DAYS, OUTPUT_PATH

def fetch_batch(url: str, state: str, start: str, end: str, key: str, retries=5):
    params = {"state": state, "start": start, "end": end}
    delay = 1
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get(key, [])
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                time.sleep(delay)
                delay *= 2
            else:
                print(f"HTTP error on batch {start} to {end} for {state}: {e}")
                break
        except Exception as e:
            print(f"Error on batch {start} to {end} for {state}: {e}")
            break
    print(f"Failed after {retries} retries for batch {start} to {end} for {state}")
    return []

def daterange(start_date, end_date, step_days):
    current = start_date
    while current <= end_date:
        batch_end = min(current + timedelta(days=step_days - 1), end_date)
        yield current, batch_end
        current = batch_end + timedelta(days=1)

def main():
    all_data = []

    start_dt = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_dt = datetime.strptime(END_DATE, "%Y-%m-%d")

    for batch_start, batch_end in tqdm(daterange(start_dt, end_dt, BATCH_DAYS)):
        batch_start_str = batch_start.strftime("%Y-%m-%d")
        batch_end_str = batch_end.strftime("%Y-%m-%d")

        data = fetch_batch(STATE, batch_start_str, batch_end_str)
        all_data.extend(data)
        time.sleep(0.5)

    if not all_data:
        print("No data fetched.")
        return

    df = pd.DataFrame(all_data)
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

