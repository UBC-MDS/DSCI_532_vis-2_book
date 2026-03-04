"""Fetch current weather from Open-Meteo (no API key needed)."""

import requests


def get_weather(lat: float, lon: float):
    """Get current weather for a latitude/longitude pair."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return {k: v for k, v in data.items()}


if __name__ == "__main__":
    print(get_weather(40.7127281, -74.0060152))
