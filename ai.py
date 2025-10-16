import os
from datetime import datetime
from llama_cpp import Llama
from config import MODEL_PATH, SYSTEM_PROMPT, RDATE
from logger import log

class AIDescription:
    def __init__(self):
        self.MODEL_SHORT = os.path.join(MODEL_PATH, "gemma-3-12b-it-Q4_K_M.gguf")
        self.WEATHER_FILE = os.path.join("data", "weather_latest.txt")
        self.system_prompt = SYSTEM_PROMPT

    # === Initialize model ===
    def load_model(self) -> Llama:
        """Load local GGUF model using llama.cpp."""
        if not os.path.exists(self.MODEL_SHORT):
            raise FileNotFoundError(f"[AI] Model not found at: {self.MODEL_SHORT}")

        log("[AI] Initializing Gemma-3-12B-it (Q4_K_M) model...", "INFO")
        model = Llama(
            model_path=self.MODEL_SHORT,
            n_ctx=1024,        # context length
            n_gpu_layers=-1,   # auto GPU layers
            verbose=False
        )
        log("[AI] Model loaded successfully.", "SUCCESS")
        return model

    # === Load weather data ===
    def load_weather_data(self) -> str:
        """Read weather data from weather_latest.txt and return as text."""
        if not os.path.exists(self.WEATHER_FILE):
            log(f"[AI] Weather file not found: {self.WEATHER_FILE}", "WARNING")
            return ""

        try:
            with open(self.WEATHER_FILE, "r", encoding="utf-8") as f:
                data = f.read()
            log(f"[AI] Weather data loaded ({len(data)} characters).", "INFO")
            return data
        except Exception as e:
            log(f"[AI][ERROR] Failed to read weather data: {e}", "ERROR")
            return ""

    # === Generate weather description ===
    def generate_weather_description(self, model: Llama, weather_data: str) -> str:
        """Combine system prompt and weather data, then generate natural text description."""
        if not weather_data:
            return "[AI] No weather data to analyze."

        full_prompt = (
            f"System: {self.system_prompt}\n\n"
            f"User: Opowiedz krótko jaka jest pogoda na podstawie tych danych:\n{weather_data}\n\n"
            f"Assistant: Based on these data, describe the current weather briefly in Polish language:\n"
        )

        log(f"[AI] Generating weather description started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "INFO")
        t1 = datetime.now()

        print("\n[AI] Generating weather descryption (streaming):\n")
        response_text = ""

        try:
            output = model(
                prompt=full_prompt,
                max_tokens=300,
                temperature=0.7,
                top_p=0.95,
                stop=["User:", "System:"]
            )
            #print("[DEBUG] Raw model output: ", output)
            response = output["choices"][0]["text"].strip()
            formatted_response = response.replace(". ", "\n")
            t2 = datetime.now()
            t3 = t2 - t1
            t3_round = round(t3.total_seconds() * 1000)

            log(f"[AI] Generation copleted successfully in {t3} seconds.", "INFO")
            log("[AI] Generation completed successfully.", "SUCCESS")
            return formatted_response or "[AI] Model returned no text."
        except Exception as e:
            log(f"[AI][ERROR] Problem during generation: {e}", "ERROR")
            return "[AI] Error occurred during weather description generation."


    def save_ai_description(self, ai_response: str) -> str:
        """Save weather description to real date and latest files."""

        latest_file = os.path.join("responses", "weather_description_latest.txt")
        real_date_file = os.path.join("responses", f"weather_description_{RDATE}.txt")

        for path in (latest_file, real_date_file):
            with open(path, "w", encoding="utf-8") as f:
                f.write(ai_response)

    # === Main AI function ===
    def run_ai_weather_description(self) -> str:
        """
        Main function combining all steps:
        1. Load model
        2. Load latest weather data
        3. Generate and return weather description
        """
        log(f"=== AI Weather Module Start ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===", "INFO")
        model = self.load_model()
        weather_data = self.load_weather_data()
        description = self.generate_weather_description(model, weather_data)
        self.save_ai_description(description)
        log("=== AI Weather Module End ===\n", "INFO")
        return description