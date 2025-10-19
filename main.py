from ai import AIDescription
from weather import WeatherService
from logger import log

def main():
    log("=== WeatherAI program started ===", "INFO")

    # Initialize weather service
    weather_service = WeatherService()

    if not weather_service.set_current_location():
        log("Fetching current location failed. Using 'Cracow' as default.", "WARNING")
        weather_service.set_location_from_predefined("Cracow")

    # Fetch, process and save weather report
    report = weather_service.get_formatted_report()

    if report and "Error" not in report:
        # Print report to console
        print("***REPORT***\n", report, "\n***END OF REPORT***")

        # Run AI Code
        aiDescription = AIDescription()
        response = aiDescription.run_ai_weather_description()

    else:
        log("Failed to generate report. Please check error logs.", "ERROR")
        print("Failed to generate report.")

    log("=== WeatherAI program ended ===\n", "INFO")

if __name__ == "__main__":
    main()