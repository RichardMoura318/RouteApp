import requests
import os
from urllib.parse import quote_plus
from config.settings import TOMTOM_API_KEY


BASE_URL = "https://api.tomtom.com"


def geocoding(address: str) -> dict:
    try:
        encoded_address = quote_plus(address)
        url = f"{BASE_URL}/search/2/geocode/{encoded_address}.json"
        params = {"key": TOMTOM_API_KEY, "limit": 1}

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return {"success": False, "data": None, "error": f"HTTP {r.status_code} - {r.reason}"}

        results = r.json().get("results", [])
        if not results:
            return {"success": False, "data": None, "error": "Nenhum resultado encontrado"}

        pos = results[0]["position"]
        return {"success": True, "data": (pos["lat"], pos["lon"]), "error": None}

    except requests.RequestException as e:
        return {"success": False, "data": None, "error": str(e)}


