import location_utils
import swisseph as swe
from datetime import datetime, timedelta
from PIL import Image
import pytz
from pytz import all_timezones
import re
import _config, config
from .nakshatra_lista import nakshatras  # ha nincs még, lent adom
import speech_recognition as sr
from .models import Poszt
from .audio_kotta_tools import felismer_hang  # itt van a speech_recognition
from .ai_utils import valasz_adas       # itt hívod az OpenAI-t
import audio_kotta_tools
import postgresql
import chart_drawer
import _time_utils

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
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

#✨ ASC kiszámítás részhoroszkópokra is
def calculate_ascendant(jd_ut, latitude, longitude):
    try:
        ascmc = swe.houses(jd_ut, latitude, longitude)[0]
        return ascmc[0]  # ASC fok
    except Exception as e:
        print("Aszcendens számítási hiba:", e)
        return 0.0