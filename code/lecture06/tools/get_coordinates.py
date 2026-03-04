import requests
from typing import Dict


def get_coordinates(location: str) -> Dict[str, float]:
    base_url: str = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1,  # only return the top result
        "addressdetails": 1,  # include detailed address info
    }

    headers = {"User-Agent": "example_weather/1.0 (daniel.chen@posit.co)"}
    response = requests.get(
        base_url,
        params=params,
        headers=headers,
    )

    data = response.json()

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return {"lat": lat, "lon": lon}
