# WeatherAI 🌦️🤖

Aplikacja w języku Python, która pobiera dane pogodowe i wykorzystuje lokalny model językowy (LLM) do generowania opisów pogody w języku naturalnym. Projekt jest w fazie rozwoju.

## O projekcie
WeatherAI to mój prywatny projekt stworzony w celu eksploracji możliwości lokalnych modeli językowych (LLM) w praktycznym zastosowaniu. Celem było połączenie danych z zewnętrznego API (pogodowego) z biblioteką `llama-cpp-python` do generowania naturalnych opisów na podstawie surowych danych.

Aplikacja potrafi pobrać pogodę dla konkretnego miasta lub dla bieżącej lokalizacji użytkownika, a następnie przekazuje te dane do modelu AI, który tworzy narracyjny opis.

---

## Użyte technologie
Główny stos technologiczny projektu:

* **Python 3.14**
* **llama-cpp-python**: Do obsługi i uruchamiania lokalnych modeli LLM.
* **Requests**: Do wykonywania zapytań do API pogodowego.
* **Geopy**: Do określania bieżącej lokalizacji (geolokalizacji).

---

## Instalacja i uruchomienie

⚠️ **Ważne**: Obecnie projekt **nie jest** gotowy do uruchomienia. Wymaga ręcznej konfiguracji pliku `config.py`, który celowo nie został dołączony do repozytorium.