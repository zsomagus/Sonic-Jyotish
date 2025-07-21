import librosa
import soundevice as sd
import soundfile as sf
import _config
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from config import full_pada_table, jegy_uralkodok, mantra_map, nakshatras, bolygo_nakshatra_map
import astro_utils

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]

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
    
    pdf_path = os.path.join("static", "kottak", filename)
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
def save_combined_wave(planet_positions, fill_prashna_data, calculate_varshaphala_chart):
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

# 🔊 Hangbetöltés
amb_y, amb_sr = librosa.load(ambiance_path, sr=None)
harang_y, harang_sr = librosa.load(harang_path, sr=None)

# 📏 Skálázás

def pitch_shift_to_hz(y, sr, target_freq, base_freq=440):
    n_steps = 12 * np.log2(target_freq / base_freq)
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

def scale_pitch(sound, orig_freq, target_freq, sr):
    ratio = target_freq / orig_freq
    new_sr = int(sr * ratio)
    resampled = librosa.resample(sound, orig_sr=sr, target_sr=new_sr)
    return resampled

engine = pyttsx3.init()
engine.setProperty('rate', 120)
