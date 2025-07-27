import numpy as np
import pandas as pd
from _config import full_pada_table, jegy_uralkodok, mantra_map, nakshatras, bolygo_nakshatra_map
from _config import varga_factor, nakshatras
import astro_chart, audio_kotta_tools
# 📆 Adatgyűjtő modul: bolygó + nakshatra + pada + jegy + ház → hangfrekvencia mentése Excelbe
def export_to_excel(planet_positions, filename="hang_adatok.xlsx"):
    import pandas as pd
    records = []

    asc_deg = planet_positions['ASC']['longitude'] % 360
    asc_sign = int(asc_deg // 30) + 1

    for planet, data in planet_positions.items():
        if planet == "ASC":
            continue
        lon = data['longitude']
        sidereal_long = lon % 360
        jegy = int(sidereal_long // 30) + 1
        haz = (jegy - asc_sign + 12) % 12 + 1

        nakshatra, pada = calculate_nakshatra(lon, ayanamsa, nakshatras)

        # Uralkodó bolygó a nakshatra-hoz
        ura = ""
        for uralkodo, lista in bolygo_nakshatra_map.items():
            if nakshatra in lista:
                ura = uralkodo
                break

        # Frekvencia keresés (pada-alapú hang)
        freq = None
        if ura in full_pada_table and nakshatra in full_pada_table[ura]:
            freqs = full_pada_table[ura][nakshatra]
            freq = freqs[pada - 1] if 0 <= (pada - 1) < len(freqs) else None

        records.append({
            "Bolygó": planet,
            "Jegy": jegy,
            "Ház": haz,
            "Nakshatra": nakshatra,
            "Nakshatra ura": ura,
            "Pada": pada,
            "Frekvencia (Hz)": freq
        })

    df = pd.DataFrame(records)
    df.to_excel(filename, index=False)
    print(f"Exportálva: {filename}")

def keres_frekvencia_excelbol(bolygo, jegy, haz, nakshatra, ura, pada):
    try:
        df = pd.read_excel("hang_adatok.xlsx")
        sor = df[
            (df['Bolygó'] == bolygo) &
            (df['Jegy'] == jegy) &
            (df['Ház'] == haz) &
            (df['Nakshatra'] == nakshatra) &
            (df['Nakshatra Ura'] == ura) &
            (df['Pada'] == pada)
        ]
        if not sor.empty:
            return float(sor.iloc[0]['Frekvencia'])
        else:
            return None
    except Exception as e:
        print(f"Excel visszakeresési hiba: {e}")
        return None