# src/scripts/realtime_fetcher.py
import time
from datetime import datetime
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

# Add the src directory to the Python path to allow imports from api
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.api import noaa_swpc
from src.api import openweathermap # Keep this if you want to use OpenWeatherMap
from src.api import openuv # Keep this if you want to use OpenUV

# Retrieve target location from environment variables
# Provide default values (e.g., Nagpur) if not set, or raise an error if critical
try:
    TARGET_LAT = float(os.getenv("TARGET_LOCATION_LAT"))
    TARGET_LON = float(os.getenv("TARGET_LOCATION_LON"))
except (ValueError, TypeError):
    print("Error: TARGET_LOCATION_LAT and TARGET_LOCATION_LON must be set in .env and be valid numbers.")
    print("Falling back to default Nagpur coordinates.")
    TARGET_LAT = 21.1458
    TARGET_LON = 79.0882


# Assuming src/db/database.py exists for later ingestion
# from src.db.database import add_raw_data_to_db # This function will be created in Step 1.2

# Define polling frequencies (in seconds)
NOAA_POLLING_INTERVAL = 60 * 1  # 1 minute for space weather
UV_POLLING_INTERVAL = 60 * 15 # 15 minutes for UV Index (applies to either OpenUV or OpenWeatherMap)


def fetch_all_realtime_data():
    """
    Fetches all defined real-time solar activity and environmental data
    for the configured target location.
    """
    print(f"\n--- Starting Real-time Data Fetch at {datetime.now().isoformat()} for Lat: {TARGET_LAT}, Lon: {TARGET_LON} ---")

    # 1. Fetch NOAA SWPC Data
    goes_xray_data = noaa_swpc.fetch_goes_xray_flux()
    dscovr_plasma_data = noaa_swpc.fetch_dscovr_plasma()
    dscovr_mag_data = noaa_swpc.fetch_dscovr_mag()
    goes_proton_flux_data = noaa_swpc.fetch_goes_proton_flux()

    # 2. Fetch UV Data for the target location
    # Choose one of the following, or fetch both if desired for redundancy/comparison
    target_uv_data = openuv.fetch_uv_data_openuv(TARGET_LAT, TARGET_LON)
    # target_uv_data = openweathermap.fetch_uv_data_openweathermap(TARGET_LAT, TARGET_LON)


    latest_data_summary = {}

    if goes_xray_data:
        latest_xray = goes_xray_data[-1] if goes_xray_data else {}
        latest_data_summary['xray_flux_latest'] = latest_xray
    if dscovr_plasma_data:
        latest_plasma = dscovr_plasma_data[-1] if dscovr_plasma_data else {}
        latest_data_summary['dscovr_plasma_latest'] = latest_plasma
    if dscovr_mag_data:
        latest_mag = dscovr_mag_data[-1] if dscovr_mag_data else {}
        latest_data_summary['dscovr_mag_latest'] = latest_mag
    if goes_proton_flux_data:
        latest_proton = goes_proton_flux_data[-1] if goes_proton_flux_data else {}
        latest_data_summary['proton_flux_latest'] = latest_proton

    if target_uv_data:
        # Key name indicates which API was used
        if 'uv' in target_uv_data: # Check if it's an OpenUV response
            latest_data_summary['target_openuv_latest'] = target_uv_data
        elif 'current' in target_uv_data: # Check if it's an OpenWeatherMap response
            latest_data_summary['target_openweathermap_latest'] = target_uv_data.get('current', {})

    print("\n--- Latest Fetched Data Summary ---")
    print(json.dumps(latest_data_summary, indent=2))
    print("--- Data Fetch Complete ---")

    return latest_data_summary

def main_polling_loop():
    """
    Main loop to continuously poll data at defined intervals for the configured location.
    """
    last_noaa_fetch_time = 0
    last_uv_fetch_time = 0

    while True:
        current_time = time.time()

        if current_time - last_noaa_fetch_time >= NOAA_POLLING_INTERVAL:
            print(f"Attempting NOAA fetch at {datetime.now().isoformat()}")
            noaa_swpc.fetch_goes_xray_flux()
            noaa_swpc.fetch_dscovr_plasma()
            noaa_swpc.fetch_dscovr_mag()
            noaa_swpc.fetch_goes_proton_flux()
            last_noaa_fetch_time = current_time

        if current_time - last_uv_fetch_time >= UV_POLLING_INTERVAL:
            print(f"Attempting UV data fetch at {datetime.now().isoformat()}")
            # Call the UV fetching function with the dynamic coordinates
            openuv.fetch_uv_data_openuv(TARGET_LAT, TARGET_LON)
            # If you were using OpenWeatherMap, you'd call:
            # openweathermap.fetch_uv_data_openweathermap(TARGET_LAT, TARGET_LON)
            last_uv_fetch_time = current_time

        # Sleep for a short period to avoid busy-waiting and allow other processes
        time.sleep(10) # Check every 10 seconds if it's time to fetch


if __name__ == '__main__':
    print("Starting real-time data fetcher...")
    try:
        main_polling_loop()
    except KeyboardInterrupt:
        print("\nReal-time data fetcher stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
