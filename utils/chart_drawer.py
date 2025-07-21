import _coordinates
import _location_utils
import matplotlib.pyplot as plt
import pytz
from pytz import all_timezones
import re
from config import varga_factor, nakshatras
import swisseph as swe
from datetime import datetime, timedelta
import pytz
from pytz import all_timezones


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
        filename = os.path.join("static", f"prashna_{now_str}_{horoszkop_nev}.png")
    else:
        filename = os.path.join("static", f"{aktualis_vezeteknev.lower()}_{aktualis_keresztnev.lower()}_horoszkop_{horoszkop_nev}.png")
        plt.savefig(filename, dpi=300, facecolor=fig.get_facecolor())
        plt.close()
        print(f"Mentve: {filename}")
        filename = os.path.join("static", f"{vezetek_nev.lower()}_{kereszt_nev.lower()}_horoszkop_{horoszkop_nev}.png")
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
