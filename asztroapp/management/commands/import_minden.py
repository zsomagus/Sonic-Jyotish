import os
import json
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from sonicjyotish.models import (
    TelepulesKoordinata,
    FelhasznaloHoroszkop,
    NakshatraInfo,
    PadaFrekvencia,
    MantraMap,
    GrahaTranzit,
    PlanetID,
    KulcsszoValasz,
    VargaFaktor,
    PurushartaMap,
    PlanetAbbreviation,
    # ... további modellek
)
import json

class Command(BaseCommand):

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"

class Command(BaseCommand):
    help = "Automatikus XLSX és JSON adatimport PostgreSQL-be"

    def handle(self, *args, **kwargs):
        # 🔹 XLSX fájlok automatikus bejárása
        xlsx_files = [f for f in os.listdir(STATIC_DIR) if f.endswith(".xlsx")]

        for filename in xlsx_files:
            file_path = STATIC_DIR / filename
            try:
                workbook = pd.read_excel(file_path, sheet_name=None)
                self.stdout.write(self.style.WARNING(f"📄 Feldolgozás: {filename}"))

                for sheet_name, df in workbook.items():
                    self.import_sheet(sheet_name, df)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"⚠️ Hiba a(z) {filename} beolvasásakor: {e}"))

        # 🔹 JSON fájl beolvasása (ha van)
        json_path = STATIC_DIR / "mentett_adatok.json"
        if json_path.exists():
            try:
                with open(json_path, encoding="utf-8") as f:
                    adatok = json.load(f)
                for item in adatok:
                    FelhasznaloHoroszkop.objects.get_or_create(
                        vezetek_nev=item["vezetek_nev"],
                        kereszt_nev=item["kereszt_nev"],
                        datum=item["datum"],
                        ido=item["ido"],
                        latitude=item["latitude"],
                        longitude=item["longitude"],
                        ido_zona=item["ido_zona"],
                        nyari_idoszamitas=item["nyari_idoszamitas"] == "igen",
                        varga=item.get("varga")
                    )
                self.stdout.write(self.style.SUCCESS("✅ JSON adatimport sikeres"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ JSON import hiba: {e}"))

        self.stdout.write(self.style.SUCCESS("🌌 Minden adat sikeresen importálva PostgreSQL-be!"))

    
        # 🔹 Mantra map
        df = sheets["mantra_map"]
        for sor in df.itertuples():
            MantraMap.objects.get_or_create(
                jegy=sor.jegyekk,
                bolygo=sor.bolygók,
                hz=sor.hz,
                mantra=sor.mantra
            )

        # 🔹 Települések
        df = sheets["file2_telepulesek"]
        for sor in df.itertuples():
            TelepulesKoordinata.objects.get_or_create(
                nev=sor.Helységnév,
                latitude=sor.Északi_szélesség,
                longitude=sor.Hosszúság
            )

        # 🔹 Nakshatra info
        df = sheets["nakshatra_info"]
        for sor in df.itertuples():
            NakshatraInfo.objects.get_or_create(
                nev=sor.Nakshatra,
                tulajdonsag=sor.Tulajdonság,
                uralkodo=sor.Uralkodó,
                mantra=sor.Mantra,
                frekvencia=sor.HZ
            )

        # 🔹 Planet abbreviations
        df = sheets["planet_abbreviations"]
        for sor in df.itertuples():
            PlanetAbbreviation.objects.get_or_create(
                nev=sor.Név,
                rovidites=sor.Rövidítés
            )

        # 🔹 Planet IDs
        df = sheets["planet_ids"]
        for sor in df.itertuples():
            PlanetID.objects.get_or_create(
                planet=sor.Planet,
                id=sor.ID
            )

        # 🔹 Tranzit adat
        df = sheets["graha_tranzit"]
        for sor in df.itertuples():
            GrahaTranzit.objects.get_or_create(
                jegy=sor.JEGY,
                asc_fugg=sor._2,  # vagy sor["ASC. FÜGGŐ"], ha van ilyen nevű attribútum
                bolygo=sor.BOLYGÓ,
                hang=sor.HANG,
                hz=sor.HZ
            )

        # 🔹 Kulcsszavas válaszok
        df = sheets["kulcsszo_valaszok"]
        for sor in df.itertuples():
            KulcsszoValasz.objects.get_or_create(
                kulcsszo=sor.Kulcsszo,
                valasz=sor._2,  # vagy Válasz szöveg
                mantra=sor._3   # Ajánlott mantra
            )

        # 🔹 Varga faktorok
        df = sheets["varga_faktor"]
        for sor in df.itertuples():
            VargaFaktor.objects.get_or_create(
                nev=sor.Név,
                hanyad=sor.Hányad,
                fok=sor["hány fok 1 jegy"]
            )

        # 🔹 Purusharta map
        df = sheets["purusharta_map"]
        for sor in df.itertuples():
            PurushartaMap.objects.get_or_create(
                haz_szam=sor["Ház száma"],
                purusharta=sor["Purusharták"]
            )
        df = sheets["bolygo_nakshatra_map"]
        for sor in df.itertuples():
            BolygoNakshatraMap.objects.get_or_create(
                bolygo=sor.bolygó,
                nakshatra1=sor.nakshatra1,
                nakshatra2=sor.nakshatra2,
                nakshatra3=sor.nakshatra3
            )
        orszaglapok = sheets["orszagok_file1"]
        for region, df in orszaglapok.items():
            for sor in df.itertuples():
                TelepulesKoordinata.objects.get_or_create(
                    nev=sor._1,
                    latitude=sor._2,
                    longitude=sor._3,
                    orszag=region
            )
        df = sheets["house_position"]
        for sor in df.itertuples():
            HousePosition.objects.get_or_create(
                jegy_szam=sor["jegyek számai"],
                jegy_nev=sor["jegyek nevei"],
                x=sor["x koordináta"],
                y=sor["y koordináta"]
            )
        df = sheets["jegy_uralkodok"]
        for sor in df.itertuples():
            JegyUralkodo.objects.get_or_create(
            jegy=sor.Jegy,
            uralkodo=sor.Uralkodó
            )
        df = sheets["nakshatra_frekvencia"]
        for sor in df.itertuples():
            NakshatraFrekvencia.objects.get_or_create(
                nakshatra=sor.Nakshatra,
                uralkodo=sor.Uralkodó,
                pada1=sor.Pada1,
                pada2=sor.Pada2,
                pada3=sor.Pada3,
                pada4=sor.Pada4
            )
        df = sheets["nakshatras"]
        for sor in df.itertuples():
            Nakshatra.objects.get_or_create(
                nev=sor.Nakshatra,
                szimbólum=sor.Szimbólum,
                energia=sor.Energia
            )# Tithi ajánlások
df = sheets["tithi_ajánlások"]
for sor in df.itertuples():
    TithiAjanlas.objects.get_or_create(
        tithi=sor.Tithi,
        ajanlas=sor.Tanácsok
    )

# Fő adatbázislap
adatbazis = sheets["asztrologiai_adatbazis"]

# Bolygók
for sor in adatbazis["Bolygók"].itertuples():
    Bolygo.objects.get_or_create(
        nev=sor.Bolygó,
        tulajdonsagok=sor.Tulajdonságok,
        napok=sor.napok,
        szamok=sor.számaik,
        növény=sor.növény,
        kristály=sor.kristály
    )

# Házak
for sor in adatbazis["Házak"].itertuples():
    Haz.objects.get_or_create(
        szam=sor._asdict()["Ház száma"],
        tulajdonsagok=sor._asdict()["Tulajdonságok"],
        uralkodo_bolygo=sor._asdict()["Uralkodó bolygó"],
        purusharta=sor._asdict()["purusharták"]
    )

# Jegyek
df = sheets["asztrológiai_adatbázis"]["Jegyek"]
for sor in df.itertuples():
    Jegy.objects.get_or_create(
        nev=sor.Jegy,
        tulajdonsagok=sor.Tulajdonságok,
        uralkodo=sor.Uralkodó
    )

# Elemek
df = sheets["asztrologiai_adatbazis"]["elemek"]
for elem in df.columns:
    tulajdonsagok = df[elem].dropna().tolist()
    Elem.objects.get_or_create(
        nev=elem,
        jellemzok=tulajdonsagok
    )

# Csakrák
df = sheets["asztrologiai_adatbazis"]["csakrák"]
for sor in df.itertuples():
    Csakra.objects.get_or_create(
        nev=sor.csakrák,
        mirigy=sor.mirigyxek,
        szin=sor.szinük,
        elem=sor.elem,
        bolygo=sor.bolygó,
        tulajdonsag=sor._6
    )

# Chara karakák
df = sheets["asztrologiai_adatbazis"]["Chara karakák"]
for sor in df.itertuples():
    CharaKaraka.objects.get_or_create(
        nev=sor.karakák,
        tulajdonsag=sor.Tulajdonságok
    )

# Nakshatra – Pada
df = sheets["asztrologiai_adatbazis"]["Nakshatra – Pada"]
for sor in df.itertuples():
    NakshatraPada.objects.get_or_create(
        nakshatra=sor.Nakshatra,
        ur=sor._asdict()["ura"],
        tulajdonsagok=sor._asdict()["Tulajdonságok"],
        mantra=sor._asdict()["mantra"],
        frekvencia=sor._asdict()["frekvencia"],
        pada1=sor._asdict()["1. Páda (Dharma)"],
        pada2=sor._asdict()["2. Páda (Artha)"],
        pada3=sor._asdict()["3. Páda (Kama)"],
        pada4=sor._asdict()["4. Páda (Moksha)"]
    )

# Vargák
df = sheets["asztrologiai_adatbazis"]["részhoroszkópok"]
for sor in df.itertuples():
    VargaInfo.objects.get_or_create(
        nev=sor.D,
        hasznalat=sor._asdict()["mire használjuk"],
        hany_fok_jegy=sor._asdict()["hány fok 1 jegy"],
        hanyad=sor.Hányad
    )

       
        self.stdout.write(self.style.SUCCESS("✅ Minden adat sikeresen importálva PostgreSQL-be!"))
