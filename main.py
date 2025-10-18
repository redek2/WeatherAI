from ai import AIDescription
from weather import WeatherService
from logger import log

def main():
    log("=== WeatherAI program started ===", "INFO")

    # Initialize weather service
    weather_service = WeatherService()

    # Fetch, process and save weather report
    report = weather_service.get_formatted_report()

    # Print report to console
    #print("***REPORT***\n", report, "\n***END OF REPORT***")

    aiDescription = AIDescription()

    response = aiDescription.run_ai_weather_description()

    # Print response to console
    #print("***AI RESPONSE***\n\n",response,"\n\n***END OF AI RESPONSE***")


    log("=== WeatherAI program ended ===\n", "INFO")

    #print("\n\n\n", modelname, "\n\n\n")

if __name__ == "__main__":
    main()

# W repozytorium ma znaleźć się config_template.py albo config.example.py, z gitignore wykluczyć katalog models/ + ogarnąć README
# Poprzenosić rzeczy do configa przerużne takie jak model i wogle