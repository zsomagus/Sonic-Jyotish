import json
from static.models import FelhasznaloHoroszkop
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sonicjyotish.settings')
django.setup()

with open("statiic/mentett_adatok.json", encoding="utf-8") as f:
    adatok = json.load(f)

for item in adatok:
    FelhasznaloHoroszkop.objects.create(
        vezetek_nev=item["vezetek_nev"],
        kereszt_nev=item["kereszt_nev"],
        datum=item["datum"],
        ido=item["ido"],
        latitude=float(item["latitude"]),
        longitude=float(item["longitude"]),
        ido_zona=item["ido_zona"],
        nyari_idoszamitas=item["nyari_idoszamitas"] == "igen",
        varga=item["varga"]
    )

print("JSON adatok sikeresen betöltve az adatbázisba!")
