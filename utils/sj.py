# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 09:27:16 2025

@author: MZs
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import numpy as np
import librosa
import sounddevice as sd
import soundfile as sf
import pyttsx3
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import swisseph as swe
import json
import pandas as pd
import pytz
from pytz import all_timezones
import re
from utils.config import get_config, load_varga
from pathlib import Path


config = get_config()
mentett_adatok = config["mentett_adatok"]
BASE_DIR = Path(__file__).resolve().parent
YANTRA_PATH = BASE_DIR / "static" / "yantra"

varga_factors = load_varga()

config_data = get_config()

last_planet_positions = None

# 🔒 Globális név-változók mentésekhez
aktualis_vezeteknev = ""
aktualis_keresztnev = ""


def calculate_ayanamsa(jd):
    """Lahiri ayanamsa számítása adott Julián dátumhoz."""
    lahiri_constant = 24.0 + (3.0 / 3600.0)
    ayanamsa = lahiri_constant + (jd - 2451545.0) * -0.0000146
    return ayanamsa


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



# Adatok betöltése JSON fájlból
def load_data():
    global data
    try:
        with open("mentett_adatok.json", "r") as file:
            data = json.load(file)
        dropdown_person["values"] = [f"{entry['vezetek_nev']} {entry['kereszt_nev']}" for entry in data]
        messagebox.showinfo("Siker", "Adatok betöltve.")
    except FileNotFoundError:
        data = []  # Üres lista, ha az adatfájl nem található
        messagebox.showerror("Hiba", "Nem található adatfájl!")

# Adatok mentése JSON fájlba

def save_data():
    new_entry = {
        "vezetek_nev": vezetek_nev_entry.get(),
        "kereszt_nev": kereszt_nev_entry.get(),
        "datum": date_entry.get(),
        "ido": time_entry.get(),
        "latitude": latitude_entry.get(),
        "longitude": longitude_entry.get(),
        "ido_zona": ido_zona_entry.get(),
        "nyari_idoszamitas": "igen" if nyari_idoszamitas_var.get() else "nem"
    }

    # 1️⃣ Előző adatok betöltése
    try:
        with open("mentett_adatok", "r", encoding="utf-8") as f:
            data = json.load(f)  # Betölti a meglévő adatokat
    except (FileNotFoundError, json.JSONDecodeError):  
        data = []  # Ha a fájl nem létezik vagy hibás, üres listát kezdünk

    # 2️⃣ Új adat hozzáadása a meglévőkhöz
    data.append(new_entry)

    # 3️⃣ Frissített lista mentése
    try:
        with open("mentett_adatok", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Siker", "Adatok mentve.")
        print("Adatok sikeresen elmentve.")
    except Exception as e:
        print(f"Hiba az adatok mentése során: {e}")
        
def set_entry(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)
        
# Adatok frissítése a mezőkben
def update_fields(event=None):
    global data
    selected_name = selected_person.get()
    selected_entry = next((entry for entry in data if f"{entry['vezetek_nev']} {entry['kereszt_nev']}" == selected_name), None)
    if selected_entry:
        set_entry(vezetek_nev_entry, selected_entry["vezetek_nev"])
        set_entry(kereszt_nev_entry, selected_entry["kereszt_nev"])
        set_entry(date_entry, selected_entry["datum"])
        set_entry(time_entry, selected_entry["ido"])
        set_entry(latitude_entry, selected_entry["latitude"])
        set_entry(longitude_entry, selected_entry["longitude"])
        set_entry(ido_zona_entry, selected_entry["ido_zona"])
        nyari_idoszamitas_var.set(selected_entry["nyari_idoszamitas"] == "igen")
        global aktualis_vezeteknev, aktualis_keresztnev
        aktualis_vezeteknev = selected_entry["vezetek_nev"]
        aktualis_keresztnev = selected_entry["kereszt_nev"]    
    else:
        messagebox.showerror("Hiba", "A kiválasztott személy adatai nem találhatók az adatbázisban.")
        

def get_coordinates(city_name, file1, file2):
    """Get coordinates for a city from Excel files"""
    try:
        # Load data from both Excel files
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # Combine dataframes
        df = pd.concat([df1, df2], ignore_index=True)
        
        # Normalize city name (lowercase)
        city_name_lower = city_name.lower()
        
        # First try exact match
        city_data = df[df['City'].str.lower() == city_name_lower]
        
        # If no exact match, try partial match
        if city_data.empty:
            city_data = df[df['City'].str.lower().str.contains(city_name_lower)]
        
        if not city_data.empty:
            # Use the first match
            first_match = city_data.iloc[0]
            
            # Handle different GPS formats
            lat = first_match['Latitude']
            lon = first_match['Longitude']
            
            # If coordinates are strings (possibly in different format), convert them
            if isinstance(lat, str) and isinstance(lon, str):
                lat = convert_coordinate_format(lat)
                lon = convert_coordinate_format(lon)
            
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"Error finding coordinates: {e}")
        return None, None

def convert_coordinate_format(coord_str):
    """Convert various coordinate formats to decimal degrees"""
    try:
        # If already decimal, return as float
        if isinstance(coord_str, (int, float)):
            return float(coord_str)
        
        # Remove spaces
        coord_str = coord_str.strip()
        
        # Check if it's already decimal format with dot
        if re.match(r'^-?\d+\.\d+$', coord_str):
            return float(coord_str)
        
        # Check if it's decimal format with comma
        if re.match(r'^-?\d+,\d+$', coord_str):
            return float(coord_str.replace(',', '.'))
        
        # Parse DMS format (e.g., "51°30'30"N")
        dms_pattern = r'(\d+)°\s*(\d+)\'?\s*(\d+)\"?\s*([NSEW])'
        match = re.match(dms_pattern, coord_str)
        
        if match:
            degrees = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            direction = match.group(4)
            
            decimal = degrees + minutes/60 + seconds/3600
            
            if direction in ['S', 'W']:
                decimal = -decimal
                
            return decimal
        
        # Parse simpler format (e.g., "51 30 N")
        simple_pattern = r'(\d+)\s+(\d+)\s+([NSEW])'
        match = re.match(simple_pattern, coord_str)
        
        if match:
            degrees = int(match.group(1))
            minutes = int(match.group(2))
            direction = match.group(3)
            
            decimal = degrees + minutes/60
            
            if direction in ['S', 'W']:
                decimal = -decimal
                
            return decimal
            
        # If none of the above, try to extract numeric values
        numeric_part = re.sub(r'[^\d.-]', '', coord_str) 
        return float(numeric_part)
        
    except Exception:
        # If conversion fails, return original value
        return coord_str
    
def get_coordinates(city_name, file1, file2):
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        df = pd.concat([df1, df2], ignore_index=True)
        city_data = df[df['City'].str.lower() == city_name.lower()]
        
        if not city_data.empty:
            return city_data.iloc[0]['Latitude'], city_data.iloc[0]['Longitude']
        else:
            return None, None
    except Exception as e:
        return None, None

def search_coordinates():
    city_name = city_entry.get()
    lat, lon = get_coordinates(city_name, 'file1.xlsx', 'file2.xlsx')
    
    if lat is not None and lon is not None:
        latitude_var.set(lat)
        longitude_var.set(lon)
    else:
        messagebox.showerror("Error", "City not found in datasets.")

def calculate_varga_positions(planet_positions, varga_factor):
    """Varga (részhoroszkóp) pozíciók számítása."""
    varga_positions = {}
    for planet, data in planet_positions.items():
        longitude = data['longitude'] % 360.0
        varga_longitude = (longitude * varga_factor) % 360.0
        varga_positions[planet] = {
            'longitude': varga_longitude
        }
    return varga_positions

def calculate_nakshatra(longitude, ayanamsa, nakshatras):
    """Nakshatra és pada számítása."""
    sidereal_longitude = (longitude - ayanamsa) % 360
    nakshatra_index = int(sidereal_longitude // 13.3333) % 27
    nakshatra = nakshatras[nakshatra_index]
    pada = int((sidereal_longitude % 13.3333) // 3.3333) + 1
    return nakshatra, pada


def calculate_varga_positions(planet_positions, varga_factor):
    varga_positions = {}
    for planet, data in planet_positions.items():
        longitude = data['longitude'] % 360.0
        varga_longitude = (longitude * varga_factor) % 360.0
        varga_positions[planet] = {
            'longitude': varga_longitude
        }
    return varga_positions


def fill_prashna_data():
    now = datetime.now()
    date_entry.delete(0, tk.END)
    date_entry.insert(0, now.strftime("%Y-%m-%d"))

    time_entry.delete(0, tk.END)
    time_entry.insert(0, now.strftime("%H:%M:%S"))

    latitude_var.set("47.4979")   # Budapest szélességi fok
    longitude_var.set("19.0402")  # Budapest hosszúsági fok

    ido_zona_var.set("Europe/Budapest")
    nyari_idoszamitas_var.set(True)
    update_utc_field()

# Főablak létrehozása
root = tk.Tk()
root.title("Hindu-Védikus asztrológiai Hang Elemző program--A kozmosz végtelen minták kárpitja várja, hogy megfejtsék – ez a program egy átjáró ehhez az égi bölcsességhez. Kozmikus önvalónk templomának hangzásviléga.")
# GUI-hoz szükséges állapotok
is_playing = False
rasi_or_varga = tk.StringVar(value="rasi")  # kapcsoló értéke: "rasi" vagy "varga"




# UI elemek létrehozása
tk.Label(root, text="Vezetéknév:").grid(row=0, column=0, padx=5, pady=5)
vezetek_nev_entry = tk.Entry(root)
vezetek_nev_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Keresztnév:").grid(row=0, column=2, padx=5, pady=5)
kereszt_nev_entry = tk.Entry(root)
kereszt_nev_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="Dátum (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Idő (HH:MM:SS):").grid(row=1, column=2, padx=5, pady=5)
time_entry = tk.Entry(root)
time_entry.grid(row=1, column=3, padx=5, pady=5)



tk.Label(root, text="Időzóna:").grid(row=3, column=0, padx=5, pady=5)
ido_zona_var = tk.StringVar()
ido_zona_entry = ttk.Combobox(root, textvariable=ido_zona_var, values=all_timezones, width=30)
ido_zona_entry.set("Europe/Budapest")  # alapértelmezett
ido_zona_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="UTC idő:").grid(row=4, column=0, padx=5, pady=5)
utc_entry = tk.Entry(root)
utc_entry.grid(row=4, column=1, padx=5, pady=5)

# Nyári időszámítás jelölőnégyzet
nyari_idoszamitas_var = tk.BooleanVar(value=False)
nyari_idoszamitas_checkbox = tk.Checkbutton(
    root, text="Érvényes", variable=nyari_idoszamitas_var)
nyari_idoszamitas_checkbox.grid(row=3, column=3, padx=5, pady=5)

# Dropdown menü a személyekhez
tk.Label(root, text="Személyek:").grid(row=4, column=0, padx=5, pady=5)
selected_person = tk.StringVar(root)
dropdown_person = ttk.Combobox(root, textvariable=selected_person)
dropdown_person.grid(row=4, column=1, padx=5, pady=5)
dropdown_person.bind("<<ComboboxSelected>>", update_fields)
# Dropdown menü a részhoroszkópokhoz
tk.Label(root, text="Részhoroszkópok:").grid(row=4, column=2, padx=5, pady=5)

selected_varga = tk.StringVar(root)
selected_varga.set('D1 (Rashi)')  # alapértelmezett

dropdown_varga = ttk.Combobox(
    root,
    textvariable=selected_varga,
    values=list(varga_factors.keys()),
    state='readonly'
)
dropdown_varga.grid(row=4, column=3, padx=5, pady=5)

save_button = tk.Button(root, text="Adatok mentése", command=save_data)
save_button.grid(row=5, column=1, padx=2, pady=10, sticky="w")

# Adatok betöltése
load_button = tk.Button(root, text="Adatok betöltése", command=mentett_adatok)
load_button.grid(row=5, column=2, padx=5, pady=10)

latitude_var = tk.StringVar()
longitude_var = tk.StringVar()


# Szélességi fok (latitude)
tk.Label(root, text="Szélességi fok (latitude) (tizedesponttal):").grid(row=2, column=0, padx=5, pady=5)
latitude_entry = tk.Entry(root, textvariable=latitude_var)
latitude_entry.grid(row=2, column=1, padx=5, pady=5)

# Hosszúsági fok (longitude)
tk.Label(root, text="Hosszúsági fok (longitude) (tizedesponttal):").grid(row=2, column=2, padx=5, pady=5)
longitude_entry = tk.Entry(root, textvariable=longitude_var)
longitude_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(root, text="Írja be a város nevét:").grid(row=2, column=4)
city_entry = tk.Entry(root)
city_entry.grid(row=2, column=5)

tk.Button(root, text="kitöltés", command=search_coordinates).grid(row=3, column=5)

# 🌀 Varshaphala – Éves horoszkóp
tk.Label(root, text="Életkor (Varshaphala):").grid(row=6, column=4, padx=5, pady=5)
eletkor_entry = tk.Entry(root)
eletkor_entry.grid(row=6, column=5, padx=5, pady=5)

tk.Button(root, text="Varshaphala készítése", command=lambda: calculate_varshaphala_chart()).grid(row=5, column=5, padx=5, pady=5)
# Gomb hozzáadása a felülethez
tk.Button(root, text="⏱ Prashna (Most horoszkóp)", command=fill_prashna_data).grid(row=5, column=3, padx=5, pady=10)

    

                    
def convert_to_utc(date_str, time_str, tz_str):
    """
    date_str: 'YYYY-MM-DD'
    time_str: 'HH:MM:SS'
    tz_str: például 'Europe/Budapest'
    """
    # Naiv datetime objektum létrehozása
    naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    # Időzóna objektum létrehozása
    tz = pytz.timezone(tz_str)
    # Lokalizálás (figyelembe veszi a DST-et)
    local_dt = tz.localize(naive_dt)
    # UTC-re konvertálás
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt

# Példa használat:
    date_input = date_entry.get()    # Például: "2025-06-01"
    time_input = time_entry.get()      # Például: "12:00:00"
    tz_input = ido_zona_entry.get()     # Például: "Europe/Budapest"

    utc_datetime = convert_to_utc(date_input, time_input, tz_input)
    print("UTC idő:", utc_datetime)

def update_utc_field():
    date_input = date_entry.get().strip()
    time_input = time_entry.get().strip()
    tz_input = ido_zona_entry.get().strip()
    if not (date_input and time_input and tz_input):
        messagebox.showerror("Hiba", "Kérlek, töltsd ki a dátum, idő és időzóna mezőket!")
        return
    try:
        utc_dt = convert_to_utc(date_input, time_input, tz_input)
        # Tegyük fel, hogy van egy utc_entry meződ, amelybe kiírjuk az eredményt
        utc_entry.delete(0, tk.END)
        utc_entry.insert(0, utc_dt.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        messagebox.showerror("Hiba", f"Konverziós hiba: {e}")

def on_tz_change(event):
    update_utc_field()

# Kötjük az eseményt az időzóna beviteli mezőhöz
    ido_zona_entry.bind("<FocusOut>", on_tz_change)
    
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
def rajzol_del_indiai_horoszkop(planet_positions, tithi, horoszkop_nev="D1"):
    fig, ax = plt.subplots(figsize=(6, 6))
    
    
# Kép mentése
  
    # Zöld rács - csak a 12 ház köré (kihagyjuk a középső 4 mezőt)
    exclude_coords = [(1, 1), (2, 1), (1, 2), (2, 2)]  # középső mezők

    for x in range(4):
        for y in range(4):
            if (x, y) not in exclude_coords:
            # Rajzoljuk meg a négyzet keretét
                ax.plot([x, x+1], [y, y], color='green', linewidth=2)       # alsó oldal
                ax.plot([x+1, x+1], [y, y+1], color='green', linewidth=2)   # jobb oldal
                ax.plot([x+1, x], [y+1, y+1], color='green', linewidth=2)   # felső oldal
                ax.plot([x, x], [y+1, y], color='green', linewidth=2)       # bal oldal


    # Háttérszín narancs
    fig.patch.set_facecolor('#FFA500')
    ax.set_facecolor('#FFA500')

    
    # Házpozíciók (dél-indiai rendszer, 1-től 12-ig)
    house_positions = {
    1: (1, 3),   # Kos
    2: (2, 3),   # Bika
    3: (3, 3),   # Ikrek
    4: (3, 2),   # Rák
    5: (3, 1),   # Oroszlán
    6: (3, 0),   # Szűz
    7: (2, 0),   # Mérleg
    8: (1, 0),   # Skorpió
    9: (0, 0),   # Nyilas
    10: (0, 1),  # Bak
    11: (0, 2),  # Vízöntő
    12: (0, 3)   # Halak
}


    # Yantra beillesztése középre
    yantra_path = find_yantra_by_tithi(tithi)
    if yantra_path:
        try:
            yantra = Image.open(yantra_path).resize((150, 150))
            ax.imshow(yantra, extent=[1.0, 3.0, 1.0, 3.0])  # középső 4 mezőt fedi le
        except Exception as e:
            print(f"Yantra megnyitási hiba: {e}")
    else:
        print(f"Nincs yantra fájl a(z) {tithi}. tithi-hez.")

    # Bolygók házba rendezése - JAVÍTOTT VERZIÓ
    house_planets = {i: [] for i in range(1, 13)}
    
    # Rövidítések létrehozása
    planet_abbreviations = {
        'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma', 'Mercury': 'Me',
        'Jupiter': 'Ju', 'Venus': 'Ve', 'Saturn': 'Sa',
        'Rahu': 'Ra', 'Ketu': 'Ke', 'ASC': 'As'
    }
    
    for planet, data in planet_positions.items():
        degrees = data["longitude"] % 360
        sign = int(degrees // 30) + 1
        if sign in house_planets:
            # Rövidítés használata
            abbreviation = planet_abbreviations.get(planet, planet[:2].upper())
            house_planets[sign].append((planet, abbreviation))

    # Bolygók megjelenítése a házakban
    for hszam, (x, y) in house_positions.items():
        bolygok = house_planets[hszam]
        for idx, (full_name, abbrev) in enumerate(bolygok):
            # Az eredeti teljes névvel keresünk a planet_positions-ben
            planet_deg = planet_positions[full_name]["longitude"] % 30
            fok = int(planet_deg)
            perc = int((planet_deg - fok) * 60)
            label = f"{abbrev} {fok}° {perc}'"
            ax.text(x + 0.5, y + 0.8 - 0.25 * idx, label,
                    ha='center', va='center', fontsize=10,
                    fontweight='bold', color='black')

    # 🔴 Átló rajzolása ASC házhoz (ha benne van az ASC)
    if "ASC" in planet_positions:
        asc_deg = planet_positions["ASC"]["longitude"] % 360
        asc_sign = int(asc_deg // 30) + 1
        if asc_sign in house_positions:
            x, y = house_positions[asc_sign]
            ax.plot([x, x + 1], [y, y + 1], color='red', linewidth=3)

    ax.set_title(f"Dél-indiai horoszkóp – {horoszkop_nev} – Tithi: {tithi}", fontsize=14, fontweight='bold')
    if "ASC" in planet_positions:
        asc_deg = planet_positions["ASC"]["longitude"] % 360
        asc_sign = int(asc_deg // 30) + 1
        rel_deg = asc_deg % 30
        print(f"ASC jegy: {asc_sign}, pozíció: {rel_deg:.2f}°")

    # Mentés fájlba
    if aktualis_vezeteknev.lower() == "prashna":
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(MENTES_DIR, f"prashna_{now_str}_{horoszkop_nev}.png")
    else:
        filename = os.path.join(MENTES_DIR, f"{aktualis_vezeteknev.lower()}_{aktualis_keresztnev.lower()}_horoszkop_{horoszkop_nev}.png")
        plt.savefig(filename, dpi=300, facecolor=fig.get_facecolor())
        plt.close()
        print(f"Mentve: {filename}")
        filename = os.path.join(MENTES_DIR, f"{vezetek_nev.lower()}_{kereszt_nev.lower()}_horoszkop_{horoszkop_nev}.png")

def calculate_ascendant(jd_ut, latitude, longitude):
    """Aszcendens (Lagna) kiszámítása fokban"""
    ascmc = swe.houses(jd_ut, latitude, longitude)[0]
    return ascmc[0]  # 0 indexen az ASC fok


def draw_chart_for_current_input():
    # UTC idő
    utc_dt = convert_to_utc(date_entry.get(), time_entry.get(), ido_zona_entry.get())
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                       utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600)

    # Koordináták
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())

    # Ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Aszcendens számítása
    asc_deg = calculate_ascendant(jd_ut, latitude, longitude)
    asc_sidereal = (asc_deg - ayanamsa) % 360
    asc_sign = int(asc_sidereal // 30) + 1  # 1-től 12-ig

    # Bolygópozíciók kiszámítása
    planet_ids = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE, 'Ketu': swe.TRUE_NODE
    }

    

    planet_positions = {}
    for name, pid in planet_ids.items():
        pos, _ = swe.calc_ut(jd_ut, pid)
        sidereal_pos = (pos[0] - ayanamsa) % 360
        planet_positions[name] = {'longitude': sidereal_pos}

    rahu_pos, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
    sidereal_rahu = (rahu_pos[0] - ayanamsa) % 360
    sidereal_ketu = (sidereal_rahu + 180) % 360
    planet_positions["Rahu"] = {"longitude": sidereal_rahu}
    planet_positions["Ketu"] = {"longitude": sidereal_ketu}
    
    # Tithi számítás
    moon_long = planet_positions['Moon']['longitude']
    sun_long = planet_positions['Sun']['longitude']
    tithi = int(((moon_long - sun_long) % 360) / 12) + 1

     # 🔹 Rási horoszkóp mentése, ASC-vel
    planet_positions_with_asc = dict(planet_positions)
    planet_positions_with_asc['ASC'] = {'longitude': asc_sidereal}
    rajzol_del_indiai_horoszkop(planet_positions_with_asc, tithi, horoszkop_nev="D1")
    global last_planet_positions
    last_planet_positions = planet_positions_with_asc

     # 🔹 Kiválasztott varga
    varga_nev = selected_varga.get()
    varga_szorzo = varga_factors.get(varga_nev, 1)

    if varga_szorzo > 1:
        varga_positions = calculate_varga_positions(planet_positions, varga_szorzo)
        varga_positions['ASC'] = {'longitude': asc_sidereal}  # Hozzáadjuk az ASC-t is
        rajzol_del_indiai_horoszkop(varga_positions, tithi, horoszkop_nev=varga_nev.replace(" ", "_"))

    messagebox.showinfo("Siker", "A horoszkópok elmentve képként!")
    rahu_pos, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
    sidereal_rahu = (rahu_pos[0] - ayanamsa) % 360
    sidereal_ketu = (sidereal_rahu + 180) % 360

    planet_positions["Rahu"] = {"longitude": sidereal_rahu}
    planet_positions["Ketu"] = {"longitude": sidereal_ketu}

    
chart_button = tk.Button(root, text="Horoszkóp rajzolása", command=draw_chart_for_current_input)
chart_button.grid(row=5, column=4, padx=10, pady=10)

def calculate_varshaphala_chart():
    try:
        eletkor = int(eletkor_entry.get())
    except ValueError:
        messagebox.showerror("Hiba", "Kérlek, adj meg érvényes életkort!")
        return

    # Születési adatok
    date_str = date_entry.get()
    time_str = time_entry.get()
    tz_str = ido_zona_entry.get()
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())

    # Születési idő UTC-ben
    szul_utc = convert_to_utc(date_str, time_str, tz_str)
    jd_szul = swe.julday(szul_utc.year, szul_utc.month, szul_utc.day,
                         szul_utc.hour + szul_utc.minute / 60 + szul_utc.second / 3600)

    # Születési Nap helyzet
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    nap_pos, _ = swe.calc_ut(jd_szul, swe.SUN)
    nap_fok = nap_pos[0]

    # Cél év = születési év + életkor
    cel_ev = szul_utc.year + eletkor
    kb_return = datetime(cel_ev, szul_utc.month, szul_utc.day, szul_utc.hour, szul_utc.minute)

    # Finom keresés ±1 napos tartományban
    best_diff = 999
    best_jd = None
    for hour_shift in range(-24*2, 24*2):  # ±2 nap
        keresett = kb_return + timedelta(hours=hour_shift)
        jd_keresett = swe.julday(keresett.year, keresett.month, keresett.day,
                                 keresett.hour + keresett.minute / 60)
        pos, _ = swe.calc_ut(jd_keresett, swe.SUN)
        eltérés = abs((pos[0] - nap_fok + 180) % 360 - 180)
        if eltérés < best_diff:
            best_diff = eltérés
            best_jd = jd_keresett

    if best_jd is None:
        messagebox.showerror("Hiba", "Nem sikerült megtalálni a napvisszatérést.")
        return

    # Horoszkóp számítása
    ayanamsa = swe.get_ayanamsa_ut(best_jd)
    planet_ids = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE, 'Ketu': swe.TRUE_NODE
    }

    planet_positions = {}
    for name, pid in planet_ids.items():
        pos, _ = swe.calc_ut(best_jd, pid)
        sidereal_pos = (pos[0] - ayanamsa) % 360
        planet_positions[name] = {'longitude': sidereal_pos}

    # ASC számítás
    asc_deg = calculate_ascendant(best_jd, latitude, longitude)
    asc_sidereal = (asc_deg - ayanamsa) % 360
    planet_positions["ASC"] = {"longitude": asc_sidereal}

    # Tithi számítás
    tithi = int(((planet_positions["Moon"]["longitude"] - planet_positions["Sun"]["longitude"]) % 360) / 12) + 1

    # Horoszkóp rajzolása
    vezetek_nev = vezetek_nev_entry.get()
    kereszt_nev = kereszt_nev_entry.get()
    horoszkop_nev = f"varshaphala_{cel_ev}"
    rajzol_del_indiai_horoszkop(planet_positions, tithi, horoszkop_nev)

    messagebox.showinfo("Siker", f"Varshaphala horoszkóp mentve: {cel_ev}")


#✨ ASC kiszámítás részhoroszkópokra is
 
def calculate_ascendant(jd_ut, latitude, longitude):
    try:
        ascmc = swe.houses(jd_ut, latitude, longitude)[0]
        return ascmc[0]  # ASC fok
    except Exception as e:
        print("Aszcendens számítási hiba:", e)
        return 0.0


# 🌞 Prashna és Varshaphala horoszkópokhoz ASC számítása részhoroszkópra is

def add_asc_to_positions(planet_positions, jd_ut, latitude, longitude, ayanamsa):
    asc_deg = calculate_ascendant(jd_ut, latitude, longitude)
    asc_sidereal = (asc_deg - ayanamsa) % 360
    planet_positions['ASC'] = {'longitude': asc_sidereal}
    return planet_positions



# 🔧 Globális beállítások
MENTES_DIR = r"C:\\Users\\MZs\\Documents\\A pykódok\\asztro elemzés\\StellAsztro\\skyfield\\mentett adatok"
os.makedirs(MENTES_DIR, exist_ok=True)

engine = pyttsx3.init()
engine.setProperty('rate', 120)

# 📌 Jegy -> (Uralkodó bolygó, Frekvencia, Mantra)
mantra_map = {
    1: ("Mars", 528, "ram"),
    2: ("Venus", 639, "yam"),
    3: ("Mercury", 741, "ham"),
    4: ("Moon", 417, "vam"),
    5: ("Sun", 963, "ram"),
    6: ("Mercury", 690, "ham"),
    7: ("Venus", 583.5, "yam"),
    8: ("Mars", 472.5, "ram"),
    9: ("Jupiter", 852, "om"),
    10: ("Saturn", 369, "lam"),
    11: ("Saturn", 907.5, "aum"),
    12: ("Jupiter", 796.5, "om")
}

# 📏 Skálázás

def pitch_shift_to_hz(y, sr, target_freq, base_freq=440):
    n_steps = 12 * np.log2(target_freq / base_freq)
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

def scale_pitch(sound, orig_freq, target_freq, sr):
    ratio = target_freq / orig_freq
    new_sr = int(sr * ratio)
    resampled = librosa.resample(sound, orig_sr=sr, target_sr=new_sr)
    return resampled

# 🌓 Holdfázis kiírás

def get_fazis_info(planet_positions):
    try:
        sun_long = planet_positions['Sun']['longitude']
        moon_long = planet_positions['Moon']['longitude']
        diff = (moon_long - sun_long) % 360
        return "növekvő hold" if diff < 180 else "csökkenő hold"
    except:
        return ""
# GUI gombok és funkciók
def stop_playback():
    global is_playing
    is_playing = False
    sd.stop()
    print("Lejátszás leállítva")
    
tk.Button(root, text="⏹ Stop", command=stop_playback).grid(row=7, column=4, pady=10)

# Dinamikusan összegyűjtött hangadatok (ezeket majd a program többi része tölti fel)
kotta_adatok = {
    "Mantra": [],
    "Jegyura": [],
    "Nakshatra": [],
    "Nakshatra ura": [],
    "Pada": []
}

# 5 sáv nevei
savsorrend = ["Mantra", "Jegyura", "Nakshatra", "Nakshatra ura", "Pada"]

# Fájlmentési hely (felhasználó nevével)
def save_kotta_pdf(kotta_adatok, vezetek_nev, kereszt_nev):
    pdf_filename = f"{aktualis_vezeteknev.lower()}_{aktualis_keresztnev.lower()}_kotta_output.pdf"
    pdf_path = os.path.join("C:\\Users\\MZs\\Documents\\A pykódok\\asztro elemzés\\StellAsztro\\skyfield\\mentett adatok", pdf_filename)

    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 landscape (inch)
        ax.set_xlim(0, 10)  # időtengely (10 mp pl.)
        ax.set_ylim(0, 5)

        # Sávok rajzolása
        for i, sav in enumerate(savsorrend):
            y = 5 - i - 0.5  # 0.5-el középre a vonalak közé
            for line in range(5):
                ax.hlines(y - 0.2 + line * 0.1, 0, 10, colors='black', linewidth=0.5)
            ax.text(-0.3, y, sav, fontsize=12, fontweight='bold', va='center')

            # Hangok kirajzolása
            for (x, freq, nev) in kotta_adatok.get(sav, []):
                ax.plot(x, y + 0.05, 'ko')  # kottafej
                ax.text(x, y + 0.2, f"{nev}\n{freq}Hz", ha='center', fontsize=8)

        ax.set_xticks(range(11))
        ax.set_xticklabels([f"{i}s" for i in range(11)])
        ax.set_yticks([])
        ax.set_title("Szonifikált horoszkóp - Zenei kottázat", fontsize=14, fontweight='bold')
        ax.axis('off')

        pdf.savefig(fig)
        plt.close()

    print(f"PDF kotta mentve: {pdf_path}")
    print(json.dumps(kotta_adatok, indent=2))

    
ayanamsa = calculate_ayanamsa

# 📦 Minden collect_layer függvény egységesítve – (list, sr) tuple-t adnak vissza


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

def play_all_layers(planet_positions):
    global is_playing
    is_playing = True
    aya_val = calculate_ayanamsa(swe.julday(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day))

    # 1. rész: 1 + 2
    s1, sr1 = collect_first_layer(planet_positions)
    s2, _ = collect_second_layer(planet_positions)
    sd.play(np.concatenate(s1 + s2), samplerate=sr1)
    sd.wait()
    if not is_playing: return

    # 2. rész: 1 + 3 + 4
    s1, sr1 = collect_first_layer(planet_positions)
    s3, _ = collect_third_layer(planet_positions, aya_val)
    s4, _ = collect_fourth_layer(planet_positions, aya_val)
    sd.play(np.concatenate(s1 + s3 + s4), samplerate=sr1)
    sd.wait()
    if not is_playing: return

    # 3. rész: 1 + 5
    s1, sr1 = collect_first_layer(planet_positions)
    s5, _ = collect_fifth_layer(planet_positions)
    sd.play(np.concatenate(s1 + s5), samplerate=sr1)
    sd.wait()


# 💾 Egységesített save_combined_wave()
def save_combined_wave(planet_positions):
    global aktualis_vezeteknev, aktualis_keresztnev

    # 🔧 Ayanamsa számítás az aktuális idő alapján
    utc_dt = datetime.utcnow()
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                       utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600)
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)

    aya_val = calculate_ayanamsa(swe.julday(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day))

    s1, sr1 = collect_first_layer(planet_positions)
    s2, _ = collect_second_layer(planet_positions)
    s3, _ = collect_third_layer(planet_positions, aya_val)
    s4, _ = collect_fourth_layer(planet_positions, aya_val)
    s5, _ = collect_fifth_layer(planet_positions)

    full_wave = np.concatenate(s1 + s2 + s1 + s3 + s4 + s1 + s5)
    filename = os.path.join(MENTES_DIR, f"{aktualis_vezeteknev.lower()}_{aktualis_keresztnev.lower()}_{selected_varga.get().lower()}.wav")
    sf.write(filename, full_wave, sr1)
    print(f"Mentve: {filename}")    
    
# 📦 Minden collect_layer függvény egységesítve – (list, sr) tuple-t adnak vissza
    s3, _ = collect_third_layer(planet_positions, ayanamsa)
    s4, _ = collect_fourth_layer(planet_positions, ayanamsa)

def collect_first_layer(planet_positions):
    segments = []
    kotta_adatok["Mantra"] = []
    current_time = 0.0
    for planet, data in planet_positions.items():
        deg = data["longitude"] % 360
        sign = int(deg // 30) + 1
        if sign not in jegy_uralkodok:
            continue
        _, freq, mantra_name = mantra_map[sign]
        mantra_path = os.path.join(mantra_dir, f"{mantra_name}.wav")
        if not os.path.exists(mantra_path):
            continue
        y, sr = librosa.load(mantra_path, sr=None)
        duration = 3.0
        shifted = pitch_shift_to_hz(y, sr, freq)
        target_duration = 3.0  # másodperc
        current_duration = len(shifted) / sr
        if current_duration < target_duration:
            rate = current_duration / target_duration
            shifted = librosa.effects.time_stretch(shifted, rate)

        segments.append(shifted)
        kotta_adatok["Mantra"].append((current_time, freq, mantra_name))
        current_time += duration
    return segments, sr

def collect_second_layer(planet_positions):
    segments = []
    kotta_adatok["Jegyura"] = []
    current_time = 0.0
    for jegy in range(1, 13):
        uralkodo, freq = jegy_uralkodok[jegy]
        bolygo_deg = planet_positions.get(uralkodo, {}).get("longitude", None)
        if bolygo_deg is None:
            continue
        scaled = scale_pitch(y, orig_freq=440, target_freq=freq, sr=sr)
        duration = len(scaled) / sr
        segments.append(scaled)
        kotta_adatok["Jegyura"].append((current_time, freq, uralkodo))
        current_time += duration
    return segments, sr

def collect_third_layer(planet_positions, ayanamsa):
    segments = []
    kotta_adatok["Nakshatra"] = []
    current_time = 0.0
    for bolygo in bolygo_nakshatra_map:
        if bolygo not in planet_positions:
            continue
        longitude = planet_positions[bolygo]['longitude']
        nakshatra, _ = calculate_nakshatra(longitude, ayanamsa, nakshatras)
        if nakshatra in bolygo_nakshatra_map[bolygo]:
            scaled = scale_pitch(harang_y, orig_freq=440, target_freq=528, sr=harang_sr)
            duration = len(scaled) / harang_sr
            segments.append(scaled)
            kotta_adatok["Nakshatra"].append((current_time, 528, bolygo))
            current_time += duration
    return segments, harang_sr

def collect_fourth_layer(planet_positions, ayanamsa):
    segments = []
    kotta_adatok["Tithi"] = []
    current_time = 0.0
    for planet, data in planet_positions.items():
        lon = data['longitude']
        nakshatra, pada = calculate_nakshatra(lon, ayanamsa, nakshatras)
        freq = full_pada_table.get(pada, 440)
        scaled = scale_pitch(y, orig_freq=440, target_freq=freq, sr=sr)
        duration = len(scaled) / sr
        segments.append(scaled)
        kotta_adatok["Tithi"].append((current_time, freq, f"{planet}-{nakshatra}-p{pada}"))
        current_time += duration
    return segments, sr

def collect_fifth_layer(planet_positions):
    segments = []
    kotta_adatok["Pada"] = []
    current_time = 0.0
    asc_deg = planet_positions['ASC']['longitude'] % 360
    asc_sign = int(asc_deg // 30) + 1
    for jegy in range(1, 13):
        uralkodo, freq = jegy_uralkodok[jegy]
        if uralkodo not in planet_positions:
            continue
        bolygo_deg = planet_positions[uralkodo]['longitude'] % 360
        bolygo_sign = int(bolygo_deg // 30) + 1
        haz_pozicio = (bolygo_sign - asc_sign + 12) % 12 + 1
        scaled = scale_pitch(y, orig_freq=440, target_freq=freq, sr=sr)
        duration = len(scaled) / sr
        segments.append(scaled)
        kotta_adatok["Pada"].append((current_time, freq, f"{uralkodo}-H{haz_pozicio}"))
        current_time += duration
    return segments, sr

# Frissített play_all_layers függvény


# Végül gombkötés:
tk.Button(root, text="kotta mentése", command=lambda: save_kotta_pdf(kotta_adatok, vezetek_nev_entry.get(), kereszt_nev_entry.get())).grid(row=7, column=6, pady=10)
# Gombok
tk.Label(root, text="Hang forrás:").grid(row=6, column=0)
tk.Radiobutton(root, text="Rashi", variable=rasi_or_varga, value="rasi").grid(row=7, column=0)
tk.Radiobutton(root, text="Részhoroszkóp", variable=rasi_or_varga, value="varga").grid(row=7, column=1)

tk.Button(root, text="▶️ Play", command=lambda: play_all_layers(last_planet_positions)).grid(row=7, column=3, pady=10)
tk.Button(root, text="💾 WAV mentés", command=lambda: save_combined_wave(last_planet_positions)).grid(row=7, column=5, pady=10)

root.mainloop()

