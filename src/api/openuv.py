# src/api/openuv.py
import requests
import os
from dotenv import load_dotenv
import json # Added for pretty printing in example usage
from datetime import datetime # Already there

# Load environment variables
load_dotenv()

OPENUV_API_KEY = os.getenv("OPENUV_API_KEY")
OPENUV_BASE_URL = "https://api.openuv.io/api/v1/uv"

def fetch_uv_data_openuv(latitude: float, longitude: float):
    """
    Fetches current UV Index data for a given location from OpenUV.
    """
    if not OPENUV_API_KEY:
        print("Error: OPENUV_API_KEY not set in .env file.")
        return None

    headers = {
        'x-access-token': OPENUV_API_KEY
    }
    params = {
        'lat': latitude,
        'lng': longitude
    }

    try:
        response = requests.get(OPENUV_BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        current_uv_index = data.get('uv')
        uv_time = data.get('uv_time')

        print(f"Fetched OpenUV data for Lat: {latitude}, Lon: {longitude}. Current UV Index: {current_uv_index} at {uv_time}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenUV data for Lat: {latitude}, Lon: {longitude}: {e}")
        if response is not None and response.status_code == 403:
            print("OpenUV API returned 403 Forbidden. Check your API key or daily/monthly limits.")
        return None

if __name__ == '__main__':
    # Example usage:
    test_lat = float(os.getenv("TARGET_LOCATION_LAT", "21.1458")) # Default to Nagpur if not set
    test_lon = float(os.getenv("TARGET_LOCATION_LON", "79.0882")) # Default to Nagpur if not set

    print(f"\n--- Testing OpenUV Data Fetcher for {test_lat}, {test_lon} ---")
    uv_data = fetch_uv_data_openuv(test_lat, test_lon)
    if uv_data:
        print(f"Full OpenUV Response:")
        print(json.dumps(uv_data, indent=2))
        print(f"Current UV Index: {uv_data.get('uv')}")
        print(f"UV Index Max for today: {uv_data.get('uv_max')}")
