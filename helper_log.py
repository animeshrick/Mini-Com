import os
import logging
from datetime import datetime

# Global variable to keep the logger initialized once
_logger_initialized = False

def onion(message: str):
    """
    Logs a message to a dynamically created log file.
    The log file is stored in D:\\Projects\\python\\Mini-Com\\logs
    and named with the current date (e.g., log_20251022.txt).
    """
    global _logger_initialized

    log_dir = r"D:\Projects\python\Mini-Com\logs"
    os.makedirs(log_dir, exist_ok=True)

    # Use one log file per day
    log_filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    log_path = os.path.join(log_dir, log_filename)

    # Initialize logger only once
    if not _logger_initialized:
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filemode="a",  # append to existing file
        )

        # Also show logs in console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)

        _logger_initialized = True
        logging.info(f"Logger initialized → {log_path}")

    # Write the message to the log
    logging.info(message)
