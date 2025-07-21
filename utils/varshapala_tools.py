import chart_drawer
import swisseph as swe
from datetime import datetime, timedelta
import pytz
from pytz import all_timezones
import location_utils

def calculate_varshaphala_chart(jd, lat, lon):
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

# 🌞 Prashna és Varshaphala horoszkópokhoz ASC számítása részhoroszkópra is
def add_asc_to_positions(planet_positions, jd_ut, latitude, longitude, ayanamsa):
    asc_deg = calculate_ascendant(jd_ut, latitude, longitude)
    asc_sidereal = (asc_deg - ayanamsa) % 360
    planet_positions['ASC'] = {'longitude': asc_sidereal}
    return planet_positions
ayanamsa = calculate_ayanamsa