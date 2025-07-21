import tkinter as tk
from tkinter import messagebox, ttk
from data import save_data, load_data, set_entry, update_fields
import json
import astro_chart
import _location_utils
from _config import varga_factors
import _coordinates
import _config 
# Főablak létrehozása
root = tk.Tk()
root.title("Hindu-Védikus asztrológiai Hang Elemző program-- Kozmikus önvalónk templomának hangzásviléga.")
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
load_button = tk.Button(root, text="Adatok betöltése", command=load_data)
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

# Végül gombkötés:
tk.Button(root, text="kotta mentése", command=lambda: save_kotta_pdf(kotta_adatok, vezetek_nev_entry.get(), kereszt_nev_entry.get())).grid(row=7, column=6, pady=10)
# Gombok
tk.Label(root, text="Hang forrás:").grid(row=6, column=0)
tk.Radiobutton(root, text="Rashi", variable=rasi_or_varga, value="rasi").grid(row=7, column=0)
tk.Radiobutton(root, text="Részhoroszkóp", variable=rasi_or_varga, value="varga").grid(row=7, column=1)

tk.Button(root, text="▶️ Play", command=lambda: play_all_layers(last_planet_positions)).grid(row=7, column=3, pady=10)
tk.Button(root, text="💾 WAV mentés", command=lambda: save_combined_wave(last_planet_positions)).grid(row=7, column=5, pady=10)
# GUI gombok és funkciók
def stop_playback():
    global is_playing
    is_playing = False
    sd.stop()
    print("Lejátszás leállítva")
    
tk.Button(root, text="⏹ Stop", command=stop_playback).grid(row=7, column=4, pady=10)
chart_button = tk.Button(root, text="Horoszkóp rajzolása", command=draw_chart_for_current_input)
chart_button.grid(row=5, column=4, padx=10, pady=10)
