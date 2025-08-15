from pathlib import Path
import pandas as pd
import swisseph as swe
from django.conf import settings

# modulok/config.py

def get_config():
    config = {
        "graha_tranzit": load_graha(),
        "nakshatra_map": load_nakshatra_map(),
        "house_position": load_house(),
        "jegy_uralkodok": load_uralkodok(),
        "kulcsszo_valaszok": load_kulcsszo(),
        "mantra_map": load_mantra_map(),
        "nakshatra_frekvencia": load_frekvencia(),
        "mentett_adatok": load_json_file(),
        "hang_adatok": load_hang(),
        "asztrológiai_adatbázis": load_adatbazis(),
        "bolygo_nakshatra_map": load_nakshatra_map(),
        "nakshatra_info": load_info(),
        "nakshatras": load_nakshatras(),
        "planet_abbreviations": load_planet_abbrev(),
        "planet_ids": load_planet_ids(),
        "tithi_ajánlások": load_tithi(),
        "varga_factors": load_varga(),
        "purusharta_map": load_purusharta(),
        "file1": load_koord1(),
        "file2": load_koord2(),
        
      #   🎵 Hangminták
        "json_path": BASE_DIR / "static" / "mentett_adatok.json",
        "mantra_dir": BASE_DIR / "static" / "mantrák",
        "ambiance_path": BASE_DIR / "static" / "hangok" / "ambiance.wav",
        "harang_path": BASE_DIR / "static" / "hangok" / "templom harang.wav",
        "galboro_path": BASE_DIR / "static" / "hangok" / "galboro.wav",
        "zaj_path": BASE_DIR / "static" / "hangok" / "zaj.wav",
    
        "YANTRA_PATH": BASE_DIR / "static" / "yantra"

            }
    hang_df = load_hang()
    config["hang_adatok"] = hang_df  # lehet üres, ha nincs fájl

    return config

BASE_DIR = Path(__file__).resolve().parent.parent
static_dir = settings.BASE_DIR / "static"

# 📁 Általános fájlok
def get_pdf_path(filename):
    return BASE_DIR / "static" / filename

YANTRA_PATH = BASE_DIR / "static" / "yantra"
swe.set_ephe_path(str(BASE_DIR / "static" / "ephe"))

# 📄 JSON fájl
def load_json_file():
    return BASE_DIR / "static" / "mentett_adatok.json"

# 📊 Excel adatfájlok
from pathlib import Path
import pandas as pd

def load_hang():
    path = BASE_DIR / "static" / "hang_adatok.xlsx"
    if path.exists():
        print("🔊 Hang adatok betöltve.")
        return pd.read_excel(path)
    else:
        print("⚠️ Nincs hang_adatok.xlsx fájl. Üres adatokat adok vissza.")
        return pd.DataFrame(columns=["jegy", "Bolygó", "Ház", "Nakshatra", "Nakshatra ura", "Pada", "frekvencia"])

def load_adatbazis():
    return pd.read_excel(BASE_DIR / "static" / "asztrológiai_adatbázis.xlsx")

def load_nakshatra_map():
    return pd.read_excel(BASE_DIR / "static" / "bolygo_nakshatra_map.xlsx")

def load_graha():
    return pd.read_excel(BASE_DIR / "static" / "graha_tranzit.xlsx")

def load_house():
    return pd.read_excel(BASE_DIR / "static" / "house_position.xlsx")

def load_uralkodok():
    return pd.read_excel(BASE_DIR / "static" / "jegy_uralkodok.xlsx")

def load_kulcsszo():
    return pd.read_excel(BASE_DIR / "static" / "kulcsszo_valaszok.xlsx")

def load_mantra_map():
    return pd.read_excel(BASE_DIR / "static" / "mantra_map.xlsx")

def load_frekvencia():
    return pd.read_excel(BASE_DIR / "static" / "nakshatra_frekvencia.xlsx")

def load_info():
    return pd.read_excel(BASE_DIR / "static" / "nakshatra_info.xlsx")

def load_nakshatras():
    return pd.read_excel(BASE_DIR / "static" / "nakshatras.xlsx")

def load_planet_abbrev():
    return pd.read_excel(BASE_DIR / "static" / "planet_abbreviations.xlsx")

def load_planet_ids():
    return pd.read_excel(BASE_DIR / "static" / "planet_ids.xlsx")

def load_tithi():
    return pd.read_excel(BASE_DIR / "static" / "tithi_ajánlások.xlsx")

def load_varga():
    return pd.read_excel(BASE_DIR / "static" / "varga_factors.xlsx")

def load_purusharta():
    return pd.read_excel(BASE_DIR / "static" / "purusharta_map.xlsx")

# 🌍 Koordináta fájlok
def load_koord1():
    return pd.read_excel(BASE_DIR / "static" / "file1.xlsx")

def load_koord2():
    return pd.read_excel(BASE_DIR / "static" / "file2.xlsx")

# 🔒 Globális név-változók
aktualis_vezeteknev = ""
aktualis_keresztnev = ""

# 🎵 Hangminták
mantra_dir = BASE_DIR / "static" / "mantrák"
ambiance_path = BASE_DIR / "static" / "hangok" / "ambiance.wav"
harang_path = BASE_DIR / "static" / "hangok" / "templom harang.wav"
galboro_path = BASE_DIR / "static" / "hangok" / "galboro.wav"
zaj_path = BASE_DIR / "static" / "hangok" / "zaj.wav"
