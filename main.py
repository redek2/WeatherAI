import lmstudio as lms
import openmeteo_requests
import os
import requests
import requests_cache
import sys
import time
import traceback
from colorama import Fore, Style, init
from datetime import datetime
from retry_requests import retry

# Paths, variables etc.
init(autoreset=True)
folder_path = r"C:\Users\redek\Desktop\WeatherAI\data"
responses_path = r"C:\Users\redek\Desktop\WeatherAI\responses"
os.makedirs(folder_path, exist_ok = True)
rdate = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_folder = r"C:\Users\redek\PycharmProjects\WeatherAI\logs"
os.makedirs(log_folder, exist_ok=True)
log_path = os.path.join(log_folder, "weather_log.txt")
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


# ----- Logs section -----
def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Log levels map
    colors = {
        "INFO": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA
    }

    color = colors.get(level.upper(), Fore.WHITE)
    formatted_message = f"[{timestamp}] [{level.upper()}] {message}"

    with open(log_path, "a", encoding = "utf-8") as f:
        f.write(formatted_message + "\n")
    print(color + formatted_message + Style.RESET_ALL)

def log_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log(f"{error_msg}", "CRITICAL")
sys.excepthook = log_exceptions

def wait_for_lmstudio(timeout=300):
    log("Connecting to LMStudio", "INFO")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get("http://localhost:1234/v1/models").json()
            models = [m.get("id") for m in r.get("data", [])]
            if any(m in models for m in ["gemma-3-12b-it", "google/gemma-3-12b"]):
                log("LMStudio is ready and model gemma-3-12b-it is loaded.", "SUCCESS")
                return True
            else:
                log("LMStudio is running but model not loaded yet.", "WARNING")
        except Exception as e:
            log(f"Waiting for LMStudio... ({e})", "WARNING")
        time.sleep(5)
    log("Failed to connect or model not loaded in LMStudio", "ERROR")
    return False

log("\n=== WeatherAI program started ===\n")

# Weather parameters, current_data, daily_data
city = 'Cracow'
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 50.06,
	"longitude": 19.94,
	"daily": ["temperature_2m_min", "temperature_2m_max", "sunrise", "sunset"],
	"current": ["temperature_2m", "rain", "cloud_cover"],
	"timezone": "auto",
}
log("Parameters loaded", "INFO")

responses = openmeteo.weather_api(url, params=params)
response = responses[0]
log(f"\nDownloading weather data for: {response.Latitude()}°N {response.Longitude()}°E, {city}", "INFO")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_time = datetime.fromtimestamp(current.Time()).strftime("%Y-%m-%d %H:%M:%S")
current_temperature_2m = current.Variables(0).Value()
current_rain = current.Variables(1).Value()
current_cloud_cover = current.Variables(2).Value()

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_sunrise = daily.Variables(2).ValuesInt64AsNumpy()
daily_sunset = daily.Variables(3).ValuesInt64AsNumpy()

log("Weather data downloaded...", "INFO")

# Weather data - save to file
try:
    report_data = (
        f"\nWeather report for {city}:\n"
        f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n"
        f"Report date: {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\n"
        "\n*Current means last open-meteo report time*\n"
        f"Current time: {current_time}\n"
        f"Current temperature_2m: {current_temperature_2m:.1f}\n"
        f"Current rain: {current_rain}mm\n"
        f"Current cloud_cover: {current_cloud_cover:.0f}%\n"
        f"\nToday min temperature: {daily_temperature_2m_min[0]:.1f}\n"
        f"Today max temperature: {daily_temperature_2m_max[0]:.1f}\n"
        f"Today sunrise: {datetime.fromtimestamp(daily_sunrise[0])}\n"
        f"Today sunset: {datetime.fromtimestamp(daily_sunset[0])}\n"
    )

    with open(f'{folder_path}/weather_{rdate}.txt', 'w') as f:
        f.write(report_data)
    with open(f'{folder_path}/weather_latest.txt', 'w') as f:
        f.write(report_data)

    log(f"Weather report for {city} saved...", "INFO")

except Exception as e:
    with open(os.path.join(folder_path, "error.log"), 'a', encoding="utf-8-sig") as logEx:
        logEx.write(f"{datetime.now().strftime("%Y-%m-%d %H-%M-%S")} - {e}\n")
    log("Error in weather data saving...", "ERROR")

# ----- AI response part -----
if wait_for_lmstudio():
    with open(f'{folder_path}/weather_latest.txt', 'r') as f:
        usedata = f.read()

    # Models: "gemma-3-12b-it"; "deepseek-r1-0528-qwen3-8b"; "llama-2-13b-chat"
    # Gemma works the best for now
    model = lms.llm("google/gemma-3-12b")
    log(f"Loading model {model}", "INFO")

    system_prompt = (
        "Jesteś asystentem pogodowym. Twój cel to tworzyć krótkie i zrozumiałe opisy pogody na podstawie danych wejściowych. "
        "Zawsze podawaj: czas raportu, temperaturę, opady, zachmurzenie, wschód i zachód słońca."
        "Dane odnoszą się do pojedynczego pomiaru. "
        "Odpowiadaj w języku polskim, maksymalnie w kilku zdaniach. Nie dodawaj niczego, czego nie ma w danych."
    )

    user_prompt = (
        f"Opowiedz krótko jaka jest pogoda w Krakowie na podstawie poniższych danych:\n\n{usedata}"
    )

    full_prompt = system_prompt + "\n\n" + user_prompt

    filetime = datetime.now().strftime("%H:%M:%S")
    response = model.respond(full_prompt)

    formatted_response = f"Jest godzina {filetime}\n\n" + str(response).replace(". ", ".\n")
    log("Formatted response is done...")

    try:
        with open(f'{responses_path}/weather-descryption_{rdate}.txt', 'w') as f:
            f.write(str(formatted_response))
        with open(f'{responses_path}/weather-descryption_latest.txt', 'w') as f:
            f.write(str(formatted_response))
        log("Response is done and written in files...")

        notepad_path = r"C:\Users\redek\Desktop\WeatherAI\responses\weather-descryption_latest.txt"
        os.startfile(notepad_path)
        log("Notepad.exe started...")

    except Exception as e:
        with open(f'{responses_path}/error.log', 'a', encoding="utf-8-sig") as logEx:
            logEx.write(f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')} - {e}\n")
        print("\n***RESPONSE ERROR***\n")
        log("Error in response...")

log("\n=== WeatherAI program ended ===\n")