import chart_drawer
import swisseph as swe
from datetime import datetime, timedelta
import pytz
from pytz import all_timezones
import location_utils


def fill_prashna_data(jd, lon, lat):
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
# 🌞 Prashna és Varshaphala horoszkópokhoz ASC számítása részhoroszkópra is
def add_asc_to_positions(planet_positions, jd_ut, latitude, longitude, ayanamsa):
    asc_deg = calculate_ascendant(jd_ut, latitude, longitude)
    asc_sidereal = (asc_deg - ayanamsa) % 360
    planet_positions['ASC'] = {'longitude': asc_sidereal}
    return planet_positions
ayanamsa = calculate_ayanamsa