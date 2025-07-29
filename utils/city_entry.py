import requests
def keres_koordinata(varosnev):
    url = f"https://nominatim.openstreetmap.org/search?city={varosnev}&format=json"
    resp = requests.get(url)
    adat = resp.json()
    if adat:
        return adat[0]['lat'], adat[0]['lon']
    else:
        return None, None