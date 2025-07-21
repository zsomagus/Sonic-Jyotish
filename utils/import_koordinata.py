# a projekt gyökérkönyvtárában hozd létre

import pandas as pd
from asztroapp.models import TelepulesKoordinata

# Megnyitjuk mindkét fájlt
for file in ["static/file1.xlsx", "static/file2.xlsx"]:
    df = pd.read_excel(file)

    for _, row in df.iterrows():
        TelepulesKoordinata.objects.get_or_create(
            nev=row['Nev'],  # vagy 'Varos' – attól függ, hogy hívják
            orszag=row.get('Orszag', ''),
            latitude=row['Latitude'],
            longitude=row['Longitude']
        )

print("Koordináták betöltve az adatbázisba.")
