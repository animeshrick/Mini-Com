import os
import logging
from datetime import datetime
from typing import Optional

# Store initialized loggers so each file has its own instance
_initialized_loggers = {}

def onion(file: Optional[str], message: str):
    """
    Logs a message to a dynamically created log file.
    The log file is stored in 'D:/Projects/python/Mini-Com/logs'
    (or a relative 'logs' directory if not found),
    and named with the current date (e.g., log_20251105.txt).
    """

    base_log_dir = r"D:\python-project\dukan\logs"
    os.makedirs(base_log_dir, exist_ok=True)

    # Determine filename based on date
    date_str = datetime.now().strftime("%Y%m%d")
    log_filename = f"{file or 'log'}_{date_str}.txt"
    log_path = os.path.join(base_log_dir, log_filename)

    # Initialize a new logger only once per log file
    if log_path not in _initialized_loggers:
        logger = logging.getLogger(log_path)
        logger.setLevel(logging.INFO)

        # File handler (append mode)
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Mark logger as initialized
        _initialized_loggers[log_path] = logger
        logger.info(f"Logger initialized → {log_path}")
    else:
        logger = _initialized_loggers[log_path]

    # Write the message to the log
    logger.info(message)
