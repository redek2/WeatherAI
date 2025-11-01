# WeatherAI

Aplikacja desktopowa (GUI) w języku Python, która pobiera aktualne dane pogodowe i wykorzystuje lokalny model językowy (LLM) do generowania opisu pogody w języku naturalnym. Projekt wykorzystuje `customtkinter` do obsługi interfejsu użytkownika oraz `llama-cpp-python` do inferencji modelu.

---

## 🇵🇱 Wersja Polska

### O projekcie

WeatherAI to aplikacja stworzona w celu eksploracji możliwości lokalnych modeli językowych (LLM) w praktycznym zastosowaniu. Aplikacja łączy dane z zewnętrznego API pogodowego (Open-Meteo) z biblioteką `llama-cpp-python` do generowania płynnych, naturalnych opisów na podstawie surowych danych.

Wersja ta posiada graficzny interfejs użytkownika (GUI), który pozwala na wygenerowanie raportu po kliknięciu przycisku. Proces generowania AI odbywa się w osobnym wątku, dzięki czemu aplikacja pozostaje responsywna.

### Zrzut ekranu

*(Zalecane: Wstaw tutaj zrzut ekranu aplikacji, aby pokazać GUI)*

`![WeatherAI GUI](./screenshot.png)`

### Główne funkcje

* **Graficzny Interfejs Użytkownika**: Prosty i nowoczesny interfejs (GUI) stworzony w `customtkinter`.
* **Pobieranie danych pogodowych**: Integracja z API Open-Meteo do pobierania aktualnych prognoz.
* **Wykrywanie lokalizacji**: Automatyczne wykrywanie lokalizacji użytkownika na podstawie adresu IP (za pomocą `geocoder`) lub możliwość ręcznego ustawienia miasta w konfiguracji.
* **Lokalne generowanie AI**: Wykorzystanie `llama-cpp-python` do uruchamiania modeli LLM (w formacie GGUF) lokalnie na maszynie użytkownika.
* **Wielowątkowość**: Proces generowania opisu przez AI działa w osobnym wątku, nie blokując interfejsu użytkownika.
* **Logowanie**: Szczegółowe logowanie zdarzeń do konsoli (z kolorami) oraz do pliku, w tym globalna obsługa wyjątków.

### Użyte technologie

* **Python 3.10+**
* **customtkinter**: Do budowy nowoczesnego interfejsu graficznego.
* **llama-cpp-python**: Do ładowania i uruchamiania modeli LLM w formacie GGUF.
* **openmeteo-requests**: Klient API dla Open-Meteo.
* **geocoder**: Do automatycznego wykrywania lokalizacji na podstawie IP.
* **colorama**: Do kolorowania logów w konsoli.
* **requests-cache** & **retry-requests**: Do buforowania i ponawiania zapytań API.

### Instalacja i konfiguracja

**Ważne**: Aby uruchomić projekt, konieczna jest ręczna konfiguracja.

1.  **Klonuj repozytorium:**
    ```
    git clone [https://github.com/TWOJA_NAZWA_UŻYTKOWNIKA/WeatherAI.git](https://github.com/TWOJA_NAZWA_UŻYTKOWNIKA/WeatherAI.git)
    cd WeatherAI
    ```

2.  **Stwórz i aktywuj wirtualne środowisko** (zalecane):
    ```
    python -m venv venv
    source venv/bin/activate  # Na Windows: venv\Scripts\activate
    ```

3.  **Zainstaluj wymagane biblioteki:**
    ```
    pip install -r requirements.txt
    ```

4.  **Pobierz model LLM:**
    * Projekt wymaga modelu językowego w formacie **GGUF**.
    * Możesz pobrać model kompatybilny z `llama.cpp`, na przykład jeden z modeli "Bielik" z Hugging Face.
    * Umieść pobrany plik `.gguf` w folderze `models/` (utwórz ten folder, jeśli nie istnieje).

5.  **Skonfiguruj aplikację (Kluczowy krok):**
    * Znajdź plik `config_template.py` w głównym katalogu.
    * Stwórz kopię tego pliku i zmień jej nazwę na `config.py`.
    * Otwórz `config.py` w edytorze tekstu.
    * Zaktualizuj zmienną `MODEL_SHORT`, aby wskazywała na plik Twojego modelu, np.:
        ```python
        MODEL_SHORT = os.path.join(MODEL_PATH, "Bielik-11B-v2.6-Instruct.Q4_K_M.gguf")
        ```
    * Dostosuj `SYSTEM_PROMPT` i `USER_PROMPT` do swoich potrzeb lub innego modelu.
    * Dodaj własne predefiniowane miasta do słownika `CITIES`, lub odkomentuj funkcję dotyczącą lokalizacji.

### Uruchamianie

Po poprawnej instalacji i konfiguracji, uruchom aplikację za pomocą pliku `gui.py`:

python gui.py
# WeatherAI

A desktop application (GUI) in Python that fetches current weather data and uses a local language model (LLM) to generate a weather description in natural language. The project uses `customtkinter` for the user interface and `llama-cpp-python` for model inference.

---

## 🇬🇧 English Version

### About The Project

WeatherAI is an application created to explore the possibilities of local language models (LLMs) in a practical application. The application combines data from an external weather API (Open-Meteo) with the `llama-cpp-python` library to generate fluent, natural descriptions from raw data.

This version features a graphical user interface (GUI) that allows generating a report at the click of a button. The AI generation process runs in a separate thread, ensuring the application remains responsive.

### Screenshot

*(Recommended: Insert a screenshot of the application here to showcase the GUI)*

`![WeatherAI GUI](./screenshot.png)`

### Key Features

* **Graphical User Interface**: A simple and modern interface (GUI) created in `customtkinter`.
* **Weather Data Fetching**: Integration with the Open-Meteo API to download current forecasts.
* **Location Detection**: Automatic detection of the user's location based on IP address (using `geocoder`) or the ability to manually set a city in the configuration.
* **Local AI Generation**: Use of `llama-cpp-python` to run LLM models (in GGUF format) locally on the user's machine.
* **Multi-threading**: The AI description generation process runs in a separate thread, not blocking the user interface.
* **Logging**: Detailed logging of events to the console (with colors) and to a file, including global exception handling.

### Technologies Used

* **Python 3.10+**
* **customtkinter**: For building the modern graphical interface.
* **llama-cpp-python**: For loading and running LLM models in GGUF format.
* **openmeteo-requests**: API client for Open-Meteo.
* **geocoder**: For automatic IP-based location detection.
* **colorama**: For coloring console logs.
* **requests-cache** & **retry-requests**: For caching and retrying API requests.

### Installation and Configuration

**Important**: Manual configuration is required to run the project.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/WeatherAI.git](https://github.com/YOUR_USERNAME/WeatherAI.git)
    cd WeatherAI
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download an LLM Model:**
    * The project requires a language model in **GGUF format**.
    * You can download a `llama.cpp`-compatible model, for example, one of the "Bielik" models from Hugging Face.
    * Place the downloaded `.gguf` file in the `models/` folder (create this folder if it doesn't exist).

5.  **Configure the Application (Key Step):**
    * Find the `config_template.py` file in the main directory.
    * Create a copy of this file and rename it to `config.py`.
    * Open `config.py` in a text editor.
    * Update the `MODEL_SHORT` variable to point to your model's file, e.g.:
        ```python
        MODEL_SHORT = os.path.join(MODEL_PATH, "Bielik-11B-v2.6-Instruct.Q4_K_M.gguf")
        ```
    * Adjust `SYSTEM_PROMPT` and `USER_PROMPT` to your needs or a different model.
    * Add your own predefined cities to the `CITIES` dictionary, or uncomment the function related to location.

### Usage

After correct installation and configuration, run the application using the `gui.py` file:

```
python gui.py