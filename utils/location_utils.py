import pandas as pd
import re
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 🔁 Alapértelmezett fájlnevek – ha nem adsz meg másikat, ezek lesznek használva
DEFAULT_FILE1 = "file1.xlsx"
DEFAULT_FILE2 = "file2.xlsx"

def get_coordinates(city_name, file1=DEFAULT_FILE1, file2=DEFAULT_FILE2):
    """
    Keresés két Excel fájlban a város nevére.
    Visszatér: (latitude, longitude) vagy (None, None)
    """
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        df = pd.concat([df1, df2], ignore_index=True)

        city_name_lower = city_name.strip().lower()

        # Elsőként próbálkozzunk pontos egyezéssel
        match = df[df['City'].str.lower() == city_name_lower]

        # Ha nincs, próbáljunk részleges egyezést
        if match.empty:
            match = df[df['City'].str.lower().str.contains(city_name_lower)]

        if not match.empty:
            lat = match.iloc[0]['Latitude']
            lon = match.iloc[0]['Longitude']

            return _normalize_coord(lat), _normalize_coord(lon)

    except Exception as e:
        print(f"Hiba a koordináta-keresés során: {e}")
    return None, None

def _normalize_coord(coord):
    """
    Konvertál különböző formátumú koordinátákat decimálissá.
    Példák: '51.5', '51,5', '51°30\'N'
    """
    try:
        if isinstance(coord, float) or isinstance(coord, int):
            return float(coord)
        coord = str(coord).strip()

        # tizedes vessző → pont
        coord = coord.replace(",", ".")

        # ha már decimális
        if re.match(r"^-?\d+\.\d+$", coord):
            return float(coord)

        # DMS-formátum: "51°30'30\"N"
        match = re.match(r"(\d+)[°º]\s*(\d+)[\'′]?\s*(\d+)?[\"″]?\s*([NSEW])", coord)
        if match:
            deg = int(match.group(1))
            min_ = int(match.group(2))
            sec = int(match.group(3)) if match.group(3) else 0
            direction = match.group(4).upper()
            decimal = deg + min_ / 60 + sec / 3600
            if direction in ["S", "W"]:
                decimal *= -1
            return decimal

        # fallback: csak számot szedünk ki
        coord = re.sub(r"[^\d\.-]", "", coord)
        return float(coord)

    except Exception:
        return None

def index_view(request):
    if request.method == "POST":
        city = request.POST.get("hely")
        lat, lon = get_coordinates(city)

        context = {
            "latitude": lat,
            "longitude": lon,
            "city": city,
            
        }
        return render(request, "index.html", context)

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

