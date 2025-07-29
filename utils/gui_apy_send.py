import requests

def regisztracio_api_kuldes():
    data = {
        "email": email_entry.get(),
        "first_name": vezetek_nev_entry.get(),
        "last_name": kereszt_nev_entry.get(),
        "szuletesi_datum": date_entry.get(),
        "szuletesi_ido": time_entry.get(),
        "szuletesi_hely": city_entry.get(),
        "latitude": latitude_entry.get(),
        "longitude": longitude_entry.get()
        # ... további mezők
    }
    url = "http://localhost:8000/api/regisztracio/"
    resp = requests.post(url, json=data)
    if resp.ok:
        messagebox.showinfo("Siker", "Regisztráció elküldve!")
    else:
        messagebox.showerror("Hiba", "Sikertelen regisztráció!")