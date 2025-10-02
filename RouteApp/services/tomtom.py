import requests
from config.settings import TOMTOM_API_KEY

baseUrl = 'https://api.tomtom.com'


def geocode(address):
    url = f"{baseUrl}/search/2/geocode/{address}.json"
    params = {"key": TOMTOM_API_KEY, "limit": 1}
    r = requests.get(url, params=params)
    if r.status_code != 200 or not r.json().get("results"):
        return None
    pos = r.json()["results"][0]["position"]
    return (pos["lat"], pos["lon"])


def routepoints(origem, destino):
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origem[0]},{origem[1]}:{destino[0]},{destino[1]}/json"
    params = {"key": TOMTOM_API_KEY, "traffic": "false"}
    r = requests.get(url, params=params)

    if r.status_code != 200:
        print(f"Erro na API TomTom: {r.status_code}")
        return []

    data = r.json()
    points = []
    for leg in data["routes"][0]["legs"]:
        for p in leg["points"]:
            points.append((p["latitude"], p["longitude"]))
    return points