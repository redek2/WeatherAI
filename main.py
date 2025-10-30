# main.py
from ai import AIDescription
from weather import WeatherService
from logger import log

def run_weather_pipeline() -> str:
    """
    Uruchamia główną logikę aplikacji: pobiera pogodę, generuje opis AI
    i zwraca go jako string.
    """
    log("=== WeatherAI program started ===", "INFO")

    # Initialize weather service
    weather_service = WeatherService()

    if not weather_service.set_current_location():
        log("Fetching current location failed. Using 'Cracow' as default.", "WARNING")
        weather_service.set_location_from_predefined("Cracow")

    # Fetch, process and save weather report
    report = weather_service.get_formatted_report()
    response_text = "Failed to generate report." # Domyślna wartość

    if report and "Error" not in report:
        # Print report to console (możesz to zostawić lub usunąć)
        #print("***REPORT***\n", report, "\n***END OF REPORT***")

        # Run AI Code
        aiDescription = AIDescription()
        response_text = aiDescription.run_ai_weather_description()

    else:
        log("Failed to generate report. Please check error logs.", "ERROR")
        # response_text już ma wartość "Failed to generate report."

    log("=== WeatherAI program ended ===\n", "INFO")
    return response_text # <-- WAŻNA ZMIANA: Zwracamy tekst

if __name__ == "__main__":
    # To pozwala nadal uruchamiać ten plik bezpośrednio, np. do testów
    print("Uruchamianie z main.py (tryb testowy)...")
    final_report = run_weather_pipeline()
    print("\n--- Otrzymany raport AI (z main.py) ---")
    print(final_report)
    print("--- Koniec raportu (z main.py) ---")