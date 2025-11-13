from datetime import datetime
from typing import Optional

# from helper.mongo_helper import MongoHelper
import logging

def onion(file: Optional[str], message: str, level: str = "INFO"):
    """Logs locally and stores logs in MongoDB synchronously."""
    logging.log(getattr(logging, level.upper(), logging.INFO), f"[{file}] {message}")

    log_data = {
        "timestamp": datetime.utcnow(),
        "level": level.upper(),
        "source": file,
        "message": message,
    }

    try:
        # MongoHelper.insert_one("app_logs", log_data)
        pass
    except Exception as e:
        logging.error(f"Failed to insert log into MongoDB: {e}")
