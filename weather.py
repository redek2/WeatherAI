import os
import requests_cache
import openmeteo_requests
import geocoder
from retry_requests import retry
from datetime import datetime
from config import DATA_PATH, CITIES, URL, PARAMS, RDATE
from logger import log


class WeatherService:
    """Handles fetching, processing and saving weather data from the Open-Meteo API."""

    def __init__(self):
        # Load configuration and initialize logger
        self.latitude = None
        self.longitude = None
        self.city_name = None
        self.data_folder = DATA_PATH

        # Setup cache and retry
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.client = openmeteo_requests.Client(session = retry_session)

        log("WeatherService initialized", "INFO")

    def get_current_location_details(self):
        try:
            g = geocoder.ip("me")

            if g.ok and g.latlng and g.city:
                location_data = {
                    "name": g.city,
                    "lat": g.latlng[0],
                    "lon": g.latlng[1]
                }
                log(f"Current location: {location_data['name']}", "INFO")
                return location_data
            else:
                log("Fetching geo data failed (g.ok=False or no data).", "ERROR")
                return None
        except Exception as e:
            log(f"Fetching geo data failed with exception: {e}", "ERROR")
            return None

    def set_location_from_predefined(self, city_name: str):
        """Ustawia lokalizację na podstawie predefiniowanego miasta z config.CITIES."""
        if city_name in CITIES:
            coords = CITIES[city_name]
            self.latitude = coords["lat"]
            self.longitude = coords["lon"]
            self.city_name = city_name  # <-- KLUCZOWE: Ustawiamy nazwę miasta
            log(f"Ustawiono lokalizację na predefiniowane miasto: {city_name}", "INFO")
            return True
        else:
            log(f"Nie znaleziono miasta: {city_name} w CITIES", "ERROR")
            return False

    def set_current_location(self):
        """Pobiera i ustawia bieżącą lokalizację urządzenia za pomocą geocodera.
        location_data = self.get_current_location_details()
        if location_data:
            self.latitude = location_data["lat"]
            self.longitude = location_data["lon"]
            self.city_name = location_data["name"]  # <-- KLUCZOWE: Ustawiamy nazwę miasta
            log(f"Ustawiono bieżącą lokalizację: {self.city_name}", "INFO")
            return True
        else:
            log("Nie udało się ustawić bieżącej lokalizacji.", "ERROR")
            return False
        """

    def fetch_weather_data(self):
        """Fetch weather data from Open-Meteo API using parameters from config or current localization."""
        if self.latitude is None or self.longitude is None:
            log("Localization (latitude/longitude) not specified", "ERROR")
            return None

        try:
            params = PARAMS.copy()
            params["latitude"] = self.latitude
            params["longitude"] = self.longitude

            log(f"Fetching weather data for: {self.city_name} ({self.latitude}, {self.longitude})", "INFO")
            responses = self.client.weather_api(URL, params = params)
            response = responses[0]
            log("Weather data successfully fetched from Open-Meteo API.", "SUCCESS")
            return response

        except Exception as e:
            log(f"Error fetching weather data: {e}", "ERROR")
            return None

    def process_weather_data(self, response) -> str:
        """Extract and format key weather information from API response."""
        if response is None:
            return "No weather data available."

        try:
            current = response.Current()
            daily = response.Daily()

            # Process current data. The order of variables needs to be the same as requested.
            current_time = datetime.fromtimestamp(current.Time()).strftime("%H:%M:%S")
            current_temperature_2m = current.Variables(0).Value()
            current_rain = current.Variables(1).Value()
            current_cloud_cover = current.Variables(2).Value()

            # Process daily data. The order of variables needs to be the same as requested.
            daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
            daily_sunrise = daily.Variables(2).ValuesInt64AsNumpy()
            daily_sunset = daily.Variables(3).ValuesInt64AsNumpy()

            if self.city_name:
                city_name = self.city_name
            else:
                city_name = "Unknown location"

            report = (
                f"Weather report for {city_name}:\n"
                f"Coordinates: {response.Latitude():.2f}°N {response.Longitude():.2f}°E\n"
                f"Actual date: {datetime.now().strftime("%Y-%m-%d")}\n"
                f"Actual time: {datetime.now().strftime("%H:%M:%S")}\n"
                f"\nLast report's conditions:\n"
                f"  Measurement time: {current_time}\n"
                f"  Temperature: {current_temperature_2m:.1f}°C\n"
                f"  Rain: {current_rain:.1f} mm\n"
                f"  Cloud cover: {current_cloud_cover:.0f}%\n\n"
                f"Today's forecast:\n"
                f"  Min temperature: {daily_temperature_2m_min[0]:.1f}°C\n"
                f"  Max temperature: {daily_temperature_2m_max[0]:.1f}°C\n"
                f"  Sunrise: {datetime.fromtimestamp(daily_sunrise[0])}\n"
                f"  Sunset: {datetime.fromtimestamp(daily_sunset[0])}"
            )

            return report

        except Exception as e:
            log(f"Error processing weather data: {e}", "ERROR")
            return "Error processing weather data."

    def save_weather_report(self, report_data: str):
        """Save the weather report to both real date and latest files."""
        try:
            os.makedirs(self.data_folder, exist_ok=True)

            file_timestamped = os.path.join(self.data_folder, f"weather_{RDATE}.txt")
            file_latest = os.path.join(self.data_folder, "weather_latest.txt")

            for path in (file_timestamped, file_latest):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(report_data)

            log(f"Weather report saved to: {file_latest}", "INFO")

        except Exception as e:
            log(f"Error saving weather report: {e}", "ERROR")

    def get_formatted_report(self) -> str:
        """Fetch, process and save the weather report, then return it as a formatted string."""
        data = self.fetch_weather_data()
        report = self.process_weather_data(data)
        self.save_weather_report(report)
        return report