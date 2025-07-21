import astro chart

def calculate_nakshatra(longitude, ayanamsa, nakshatras):
    """Nakshatra és pada számítása."""
    sidereal_longitude = (longitude - ayanamsa) % 360
    nakshatra_index = int(sidereal_longitude // 13.3333) % 27
    nakshatra = nakshatras[nakshatra_index]
    pada = int((sidereal_longitude % 13.3333) // 3.3333) + 1
    return nakshatra, pada

def find_yantra_by_tithi(tithi, yantra_folder=YANTRA_PATH):
    """
    Visszaadja a tithi-hez tartozó yantra fájl elérési útját, ha található.
    A fájlnév számjeggyel kezdődik (pl. 9 kulasundari.jpg).
    """
    for fname in os.listdir(yantra_folder):
        if fname.lower().endswith(".jpg") and fname.startswith(str(tithi)):
            return os.path.join(yantra_folder, fname)
    return None
vezetek_nev = vezetek_nev_entry.get()
kereszt_nev = kereszt_nev_entry.get()

def get_current_moon_nakshatra():
    now = datetime.utcnow()
    jd = swe.julday(now.year, now.month, now.day, 
                    now.hour + now.minute / 60 + now.second / 3600)
    moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal = (moon_pos - ayanamsa) % 360
    index = int(sidereal // (360 / 27))
    return nakshatras[index]
df = pd.read_excel("kulcsszo_valaszok.xlsx")
