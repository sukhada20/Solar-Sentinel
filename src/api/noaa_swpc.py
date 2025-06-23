# src/api/noaa_swpc.py
import requests
import json
from datetime import datetime

NOAA_BASE_URL = "https://services.swpc.noaa.gov/json/"

def fetch_goes_xray_flux():
    """Fetches GOES X-ray flux data."""
    url = f"{NOAA_BASE_URL}goes/primary/xrays-6-hour.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"Fetched GOES X-ray Flux data. Records: {len(data)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GOES X-ray Flux data: {e}")
        return None

def fetch_dscovr_plasma():
    """Fetches DSCOVR plasma data (solar wind speed, density)."""
    url = f"{NOAA_BASE_URL}dscovr/dscovr_plasma-1-minute.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched DSCOVR Plasma data. Records: {len(data)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DSCOVR Plasma data: {e}")
        return None

def fetch_dscovr_mag():
    """Fetches DSCOVR magnetic field data (IMF Bz)."""
    url = f"{NOAA_BASE_URL}dscovr/dscovr_mag-1-minute.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched DSCOVR Magnetic Field data. Records: {len(data)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DSCOVR Magnetic Field data: {e}")
        return None

def fetch_goes_proton_flux():
    """Fetches GOES proton flux data."""
    url = f"{NOAA_BASE_URL}goes/primary/goes-proton-flux-7-day.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched GOES Proton Flux data. Records: {len(data)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GOES Proton Flux data: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    print("\n--- Testing NOAA SWPC Data Fetchers ---")
    xray_data = fetch_goes_xray_flux()
    if xray_data:
        # Get the latest entry
        latest_xray = xray_data[-1] if xray_data else None
        print(f"Latest X-ray Flux: {latest_xray}")

    plasma_data = fetch_dscovr_plasma()
    if plasma_data:
        latest_plasma = plasma_data[-1] if plasma_data else None
        print(f"Latest Plasma Data: {latest_plasma}")

    mag_data = fetch_dscovr_mag()
    if mag_data:
        latest_mag = mag_data[-1] if mag_data else None
        print(f"Latest Magnetic Field Data: {latest_mag}")

    proton_data = fetch_goes_proton_flux()
    if proton_data:
        latest_proton = proton_data[-1] if proton_data else None
        print(f"Latest Proton Flux: {latest_proton}")
