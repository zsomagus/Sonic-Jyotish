import numpy as np
import pytz
import datetime

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
    ido_zona_entry.bind("<FocusOut>", on_tz_chan