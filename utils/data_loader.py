import pandas  as pd
from pathlib import Path
ADATMAPPA = Path(__file__).resolve().parent.parent / "static"
sheets["asztrologiai_adatbazis"] = pd.read_excel(ADATMAPPA / "asztrológiai_adatbázis.xlsx", sheets_name=None)


# Mappa megnevezések
ADATMAPPA = STATIC_DIR
# Csak egyszer fut le: betölti az összes adatot dictionary-ként
def load_all_xlsx():
    sheets = {}

    sheets["bolygo_nakshatra_map"] = pd.read_excel(ADATMAPPA / "bolygó_nakshatra_map.xlsx")
    sheets["file2_telepulesek"] = pd.read_excel(ADATMAPPA / "file2.xlsx")
    sheets["graha_tranzit"] = pd.read_excel(ADATMAPPA / "graha_tranzit.xlsx")
    sheets["house_position"] = pd.read_excel(ADATMAPPA / "house_position.xlsx")
    sheets["jegy_uralkodok"] = pd.read_excel(ADATMAPPA / "jegy_uralkodok.xlsx")
    sheets["kulcsszo_valaszok"] = pd.read_excel(ADATMAPPA / "kulcsszo_valaszok.xlsx")
    sheets["mantra_map"] = pd.read_excel(ADATMAPPA / "mantra_map.xlsx")
    sheets["nakshatra_info"] = pd.read_excel(ADATMAPPA / "nakshatra_info.xlsx")
    sheets["nakshatras"] = pd.read_excel(ADATMAPPA / "nakshatras.xlsx")
    sheets["planet_abbreviations"] = pd.read_excel(ADATMAPPA / "planet_abbreviations.xlsx")
    sheets["planet_ids"] = pd.read_excel(ADATMAPPA / "planet_ids.xlsx")
    sheets["tithi_ajanlasok"] = pd.read_excel(ADATMAPPA / "tithi_ajánlások.xlsx")
    sheets["varga_faktorok"] = pd.read_excel(ADATMAPPA / "varga_factor.xlsx")
    sheets["purusharta_map"] = pd.read_excel(ADATMAPPA / "purusharta_map.xlsx")
    sheets["hang_adat"] = pd.read_excel(ADATMAPPA / "hang_adatok.xlsx")
    sheets["nakshatra_frekvencia"] = pd.read_excel(ADATMAPPA / "nakshatra_frekvencia.xlsx")

    # Többfüles fájl – pl. file1.xlsx országcsoportonként
    sheets["orszagok_file1"] = pd.read_excel(ADATMAPPA / "file1.xlsx", sheets_name=None)

    return sheets

# Betöltjük a teljes fájlt
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
ADATMAPPA = STATIC_DIR

def load_all_xlsx():
    sheets = {}

    # Egyfüles fájlok
    for nev in [
        "bolygó_nakshatra_map", "file2", "graha_tranzit", "house_position",
        "jegy_uralkodok", "kulcsszo_valaszok", "mantra_map",
        "nakshatra_info", "nakshatras", "planet_abbreviations",
        "planet_ids", "tithi_ajánlások", "varga_factor", "purusharta_map",
        "hang_adatok", "nakshatra_frekvencia"
    ]:
        sheets[nev] = pd.read_excel(ADATMAPPA / f"{nev}.xlsx")

    # Többfüles fájlok
    sheets["orszagok_file1"] = pd.read_excel(ADATMAPPA / "file1.xlsx", sheets_name=None)
    sheets["asztrologiai_adatbazis"] = pd.read_excel(ADATMAPPA / "asztrológiai_adatbázis.xlsx", sheets_name=None)

    return sheets

sheets = load_all_xlsx()

                                                       
def get_frekvenciak_for_nakshatra(bolygo, nakshatra):  
    df = sheet["nakshatra_frekvencia"]
    sor = df[(df["Uralkodó"] == bolygo) & (df["Nakshatra"] == nakshatra)]
    if not sor.empty:
        return [sor["Pada1"].values[0], sor["Pada2"].values[0],
                sor["Pada3"].values[0], sor["Pada4"].values[0]]
    return None


def get_hang_adat(bolygo, nakshatra):
    df = sheet[hang_adat]           
    sor = df[(df["Bolygo"] == bolygo) & (df["Nakshatra"] == nakshatra)]
    if not sor.empty:
        return {
            "mantra": sor["Mantra"].values[0],
            "frekvencia": sor["Frekvencia"].values[0],
            "hang_fajl": sor["Hang_fajl"].values[0]
        }
    return None
def get_jegy_tulajdonsagok(jegy_nev):
    df = sheets[asztrológiai_adatbázis]["Jegyek"]
    sor = df[df["Jegy"].str.lower() == jegy_nev.lower()]
    if not sor.empty:
        return {
            "tulajdonsagok": sor["Tulajdonságok"].values[0],
            "uralkodo": sor["Uralkodó"].values[0]
        }
    return None
def get_haz_info(haz_szam):
    df = sheets[asztrológiai_adatbázis]["Házak"]
    sor = df[df["Ház száma"] == haz_szam]
    if not sor.empty:
        return {
            "tulajdonsagok": sor["Tulajdonságok"].values[0],
            "uralkodo": sor["Uralkodó bolygó"].values[0],
            "purusharta": sor["purusharták"].values[0]
        }
    return None
def get_bolygo_info(bolygo_nev):
    df = sheets[asztrológiai_adatbázis]["Bolygók"]
    sor = df[df["Bolygó"].str.lower() == bolygo_nev.lower()]
    if not sor.empty:
        return {
            "tulajdonsagok": sor["Tulajdonságok"].values[0],
            "nap": sor["napok"].values[0],
            "szám": sor["számaik"].values[0],
            "növény": sor["növény"].values[0],
            "kristály": sor["kristály"].values[0],
            "szimbólum": sor["Szimbólum"].values[0],
        }
    return None
def get_nakshatra_pada_info(nakshatra):
    df = sheets[asztrológiai_adatbázis]["Nakshatra – Pada"]
    sor = df[df["Nakshatra"].str.lower() == nakshatra.lower()]
    if not sor.empty:
        return {
            "ura": ["ura"].values[0],
            "tulajdonsagok": sor["Tulajdonságok"].values[0],
            "mantra": sor["mantra"].values[0],
            "frekvencia": sor["frekvencia"].values[0],
            "pada_1": sor["1. Páda (Dharma)"].values[0],
            "pada_2": sor["2. Páda (Artha)"].values[0],
            "pada_3": sor["3. Páda (Kama)"].values[0],
            "pada_4": sor["4. Páda (Moksha)"].values[0],
        }
    return None
def get_chara_karaka_info(karaka):
    df = sheets[asztrológiai_adatbázis]["Chara karakák"]
    sor = df[df["karakák"].str.lower() == karaka.lower()]
    if not sor.empty:
        return sor["Tulajdonságok"].values[0]
    return None
def get_varga_info(varga_nev):
    df = sheets["asztrologiai_adatbazis"]["részhoroszkópok"]
    sor = df[df["D"].str.lower() == varga_nev.lower()]
    if not sor.empty:
        return {
            "hasznalat": sor["mire használjuk"].values[0],
            "fok": sor["hány fok 1 jegy"].values[0],
            "hanyad": sor["Hányad"].values[0]
        }
    return None
def get_elem_jellemzok(elem_nev):
    df = sheets[asztrológiai_adatbázis]["elemek"]
    elem_nev = elem_nev.upper()
    if elem_nev in df.columns:
        return df[elem_nev].dropna().tolist()
    return []
def get_csakra_info(csakra_nev):
    df = sheets[asztrológiai_adatbázis]["csakrák"]
    sor = df[df["csakrák"].str.lower() == csakra_nev.lower()]
    if not sor.empty:
        return {
            "mirigy": sor["mirigyxek"].values[0],
            "szín": sor["szinük"].values[0],
            "elem": sor["elem"].values[0],
            "bolygo": sor["bolygó"].values[0],
            "tulajdonsag": sor["Tul."].values[0]
        }
    return None
def get_nakshatrak_for_bolygo(bolygo: str):
    df = sheets["bolygo_nakshatra_map"]
    sor = df[df["bolygó"].str.lower() == bolygo.lower()]
    if not sor.empty:
        return [sor["nakshatra1"].values[0], sor["nakshatra2"].values[0], sor["nakshatra3"].values[0]]
    return []
def get_orszag_info(region: str, orszag: str):
    sheet = sheets["orszagok_file1"].get(region)
    if sheet is not None:
        sor = sheet[sheet["Állam/terület"].str.lower() == orszag.lower()]
        if not sor.empty:
            return {
                "fovaros": sor["Főváros"].values[0],
                "szelesseg": sor["Szélességi  fok"].values[0],
                "hosszusag": sor["Hosszúsági fok"].values[0]
            }
    return None
def get_valasz_kulcsszora(kulcsszo: str):
    df = sheets["kulcsszo_valaszok"]
    sor = df[df["Kulcsszo"].str.lower() == kulcsszo.lower()]
    if not sor.empty:
        return {
            "valasz": sor["Válasz szöveg"].values[0],
            "mantra": sor["Ajánlott mantra"].values[0]
        }
    return None
def get_mantra_for_jegy(jegy: int):
    df = sheets["mantra_map"]
    sor = df[df["jegyekk"] == jegy]
    if not sor.empty:
        return {
            "bolygo": sor["bolygók"].values[0],
            "hz": sor["hz"].values[0],
            "mantra": sor["mantra"].values[0]
        }
    return None
def get_telepuless_koorinatak(region: str, orszag: str):
    df = sheets["file2_telepulesek"]
    sor = df[df["Helységnév"] == helységnév]
    if not sor.empty:
        return {
            "Északi szélesség": sor["Északi szélesség"].values[0],
            "Hosszúság": sor["Hosszúság"].values[0],
        }
    return None
def get_tranzit_info(jegy, asc_fugg, bolygo):
    df = sheets["graha_tranzit"]
    sor = df[
        (df["JEGY"].str.lower() == jegy.lower()) &
        (df["ASC. FÜGGŐ"].str.lower() == asc_fugg.lower()) &
        (df["BOLYGÓ"].str.lower() == bolygo.lower())
    ]
    if not sor.empty:
        return {
            "hang": sor["HANG"].values[0],
            "hz": sor["HZ"].values[0]
        }
    return None
def get_house_coordinates(jegy_szam: int):
    df = sheets["house_position"]
    sor = df[df["jegyek számai"] == jegy_szam]
    if not sor.empty:
        return {
            "x": sor["x koordináta"].values[0],
            "y": sor["y koordináta"].values[0],
            "jegy": sor["jegyek nevei"].values[0]
        }
    return None
def get_jegy_ura(jegy_nev: str):
    df = sheets["jegy_uralkodok"]
    sor = df[df["jegy"].str.lower() == jegy_nev.lower()]
    if not sor.empty:
        return {
            "ura": sor["ura"].values[0],
            "hz": sor["hz"].values[0]
        }
    return None
def get_nakshatra_info(nakshatra_nev: str):
    df = sheets["nakshatra_info"]
    sor = df[df["Nakshatra"].str.lower() == nakshatra_nev.lower()]
    if not sor.empty:
        return {
            "ura": sor["ura"].values[0],
            "tulajdonsag": sor["tulajdonság"].values[0],
            "mantra": sor["mantra"].values[0],
            "frekvencia": sor["frekvencia"].values[0]
        }
    return None
def get_nakshatra_by_number(szam: int):
    df = sheets["nakshatras"]
    sor = df[df["szám"] == szam]
    if not sor.empty:
        return sor["nakshatra"].values[0]
    return None
def get_planet_abbreviation(planet_nev: str):
    df = sheets["planet_abbreviations"]
    sor = df[df["bolygó"].str.lower() == planet_nev.lower()]
    if not sor.empty:
        return sor["rövidités"].values[0]
    return None
def get_planet_id_info(planet_nev: str):
    df = sheets["planet_ids"]
    sor = df[df["bolygó"].str.lower() == planet_nev.lower()]
    if not sor.empty:
        return {
            "szama": sor["száma"].values[0],
            "napja": sor["napja"].values[0],
            "efemerida": sor["efemerida"].values[0]
        }
    return None
def get_tithi_ajanlas(tithi_szam: int):
    df = sheets["tithi_ajánlások"]
    sor = df[df["Tithi_szám"] == tithi_szam]
    if not sor.empty:
        return {
            "tipus": sor["Tithi_tipus"].values[0],
            "nev": sor["Tithi_nev"].values[0],
            "jelentes": sor["Jelentés"].values[0],
            "ajanlas": sor["Napi_ajanlas"].values[0]
        }
    return None
def get_varga_factor(betujel: str):
    df = sheets["varga_factor"]
    sor = df[df["betüjel"].str.lower() == betujel.lower()]
    if not sor.empty:
        return {
            "reszhoroszkop": sor["részhoroszkóp"].values[0],
            "oszto": sor["osztó"].values[0]
        }
    return None
def get_hazak_for_purusharta(purusharta: str):
    df = sheets["purusharta_map"]
    sor = df[df["ppurusharta"].str.lower() == purusharta.lower()]
    if not sor.empty:
        return [int(h.strip()) for h in str(sor["házai"].values[0]).split(",")]
    return []
