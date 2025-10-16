import sys
import traceback
from datetime import datetime
from colorama import Fore, Style, init
from config import LOG_PATH

# --- Initialize colorama ---
init(autoreset=True)

# --- Logging function ---
def log(message: str, level: str = "INFO") -> None:
    """
    Logs a message to both console (with color) and log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Log level color mapping
    colors = {
        "INFO": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA
    }

    color = colors.get(level.upper(), Fore.WHITE)
    formatted_message = f"[{timestamp}] [{level.upper()}] {message}"

    # Write to file
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(formatted_message + "\n")

    # Print to console
    print(color + formatted_message + Style.RESET_ALL)


# --- Exception handler ---
def log_exceptions(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler that logs unhandled exceptions.
    """
    # Skip keyboard interrupts
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Format and log the traceback
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log(error_msg, "CRITICAL")


# --- Apply exception hook globally ---
sys.excepthook = log_exceptions