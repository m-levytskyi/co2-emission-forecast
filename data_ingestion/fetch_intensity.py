from pathlib import Path
import sys
import argparse
import requests
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import time
from urllib.parse import urljoin
import argparse

from config import BASE_URL, CONSUMPTION_INTENSITY, PRODUCTION_INTENSITY, STATE_CODES, BATCH_DAYS, DATA_DIR, DEFAULT_START_DATE, DEFAULT_END_DATE

DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_batch(url: str, state: str, start: str, end: str, key: str, 
                retries=5, base_delay=30.0, request_delay=1.0):
    """
    Simple rate-limited batch fetcher
    
    Args:
        request_delay: Seconds to wait before each request (proactive rate limiting)
        base_delay: Initial delay for retries after 429 errors
    """
    params = {"state": state, "start": start, "end": end}
    
    # Proactive rate limiting - wait before making request
    time.sleep(request_delay)
    
    delay = base_delay
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            return resp.json().get(key, [])
            
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                # Check if server provides retry-after header
                retry_after = resp.headers.get('Retry-After')
                if retry_after:
                    try:
                        delay = int(retry_after)
                    except ValueError:
                        pass
                
                time.sleep(delay)
                print(f"Rate limit exceeded, retrying in {delay} seconds...")
                delay *= 2  # Exponential backoff
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

def load_existing_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

def fetch_and_save(
    url: str,
    key: str,
    filename_suffix: str,
    start_date_str: str,
    end_date_str: str,
):
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")

    for state in STATE_CODES:
        print(f"\nFetching {filename_suffix} data for {state}...")
        file_path = DATA_DIR / f"{state}_{filename_suffix}_intensity.csv"
        existing_df = load_existing_csv(file_path)
        fetched_rows = []

        for batch_start, batch_end in tqdm(daterange(start_dt, end_dt, BATCH_DAYS)):
            batch_start_str = batch_start.strftime("%Y-%m-%d")
            batch_end_str = batch_end.strftime("%Y-%m-%d")

            if not existing_df.empty:
                existing_dates = existing_df["start"].dt.date
                needed_dates = {
                    (batch_start + timedelta(days=i)).date()
                    for i in range((batch_end - batch_start).days + 1)
                }
                if needed_dates.issubset(existing_dates):
                    continue

            data = fetch_batch(url, state, batch_start_str, batch_end_str, key)
            fetched_rows.extend(data)
            time.sleep(0.5)

        if fetched_rows:
            new_df = pd.DataFrame(fetched_rows)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.drop_duplicates(subset=["start"], inplace=True)
            combined_df.sort_values(by="start", inplace=True)
            combined_df.to_csv(file_path, index=False)
            print(f"Saved {len(combined_df)} total records to {file_path}")
        else:
            print(f"No new data for {state}.")

if __name__ == "__main__":

    consumption_url = urljoin(BASE_URL, CONSUMPTION_INTENSITY)
    production_url = urljoin(BASE_URL, PRODUCTION_INTENSITY)

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, default=DEFAULT_START_DATE)
    parser.add_argument("--end", type=str, default=DEFAULT_END_DATE)
    parser.add_argument(
        "--mode",
        choices=["consumption", "production", "both"],
        default="both",
        help="Which intensity data to fetch",
    )
    args = parser.parse_args()

    if args.mode in ("consumption", "both"):
        fetch_and_save(
            consumption_url,
            "Consumption-based Intensity (historical)",
            "consumption",
            args.start,
            args.end,
        )
    if args.mode in ("production", "both"):
        fetch_and_save(
            production_url,
            "Production-based Intensity (historical)",
            "production",
            args.start,
            args.end,
        )

