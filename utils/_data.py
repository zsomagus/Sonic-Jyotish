import json
from sonicjyotish.models import FelhasznaloHoroszkop

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
        with open("mentett_adatok.json", "r", encoding="utf-8") as f:
            data = json.load(f)  # Betölti a meglévő adatokat
    except (FileNotFoundError, json.JSONDecodeError):  
        data = []  # Ha a fájl nem létezik vagy hibás, üres listát kezdünk

    # 2️⃣ Új adat hozzáadása a meglévőkhöz
    data.append(new_entry)

    # 3️⃣ Frissített lista mentése
    try:
        with open("mentett_adatok.json", "w", encoding="utf-8") as f:
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
        
# 🔄 Adatlogika: nem tud semmit a GUI-ról
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(path, new_entry):
    data = load_json(path)
    data.append(new_entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# gui_data_logic.py
new_entry = {...}  # GUI-ból érkezett adatok
save_json(JSON_FILE, new_entry)

with open("users_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for rekord in data:
    FelhasznaloHoroszkop.objects.create(
        vezetek_nev = rekord["vezetek_nev"],
        kereszt_nev = rekord["kereszt_nev"],
        datum = rekord["datum"],
        ido = rekord["ido"],
        latitude = rekord["latitude"],
        longitude = rekord["longitude"],
        ido_zona = rekord["ido_zona"],
        nyari_idoszamitas = rekord["nyari_idoszamitas"].lower() == "igen"
    )
