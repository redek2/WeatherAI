import os
from datetime import datetime

# --- Paths ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) # Base path to project folder
DATA_PATH = os.path.join(BASE_PATH, "data") # Path to folder data in project folder
RESPONSES_PATH = os.path.join(BASE_PATH, "responses") # Path to responses folder in project folder
LOG_FOLDER = os.path.join(BASE_PATH, "logs") # Path to logs folder in project folder
LOG_PATH = os.path.join(LOG_FOLDER, "weather_log.txt") # Path to weather_log.txt (base_path/logs/weather_log.txt)
MODEL_PATH = os.path.join(BASE_PATH, "models") # Path to models folder in project folder
MODEL_SHORT = os.path.join(MODEL_PATH, "YOUR_LLM_MODEL.gguf") # Path to AI model in gguf extension located in folder models or symlink in that folder

SYSTEM_PROMPT = ("Here you can write system prompt to your LLM")
USER_PROMPT = ("Here you can write user prompt to your LLM")

backslash = chr(92)
# Ta linia automatycznie wyciągnie nazwę pliku z MODEL_SHORT
modelname = os.path.basename(MODEL_SHORT).removesuffix(".gguf")

# Creating folders if they don't exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(RESPONSES_PATH, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# --- Real date and location ---
RDATE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# --- List of cities ---
CITIES = {
    # City template:
    # "CityName": {"lat": xx.xx, "lon": yy.yy}
}

# --- API ---
URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 0.0,
    "longitude": 0.0,
    "daily": ["temperature_2m_min", "temperature_2m_max", "sunrise", "sunset"],
    "current": ["temperature_2m", "rain", "cloud_cover"],
    "timezone": "auto"
} # Check api documentation for more parameters to fetch