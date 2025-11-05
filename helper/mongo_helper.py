from dotenv import load_dotenv
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
import logging


class MongoHelper:
    _client: Optional[MongoClient] = None
    _db = None
    load_dotenv()

    @classmethod
    def _connect(cls):
        """Synchronous MongoDB connection using PyMongo."""
        if cls._client is None:
            mongo_uri = os.getenv("MONGODB_URI")
            if not mongo_uri:
                raise RuntimeError("MONGODB_URI not found in environment variables")

            cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db_name = os.getenv("MONGO_DB_NAME",)
            cls._db = cls._client[db_name]

            # Quick ping test
            try:
                cls._client.admin.command("ping")
                logging.info("✅ Connected to MongoDB successfully.")
            except Exception as e:
                logging.error(f"❌ MongoDB connection failed: {e}")
                raise
        return cls._db

    # -------------------------
    # CRUD
    # -------------------------
    @classmethod
    def insert_one(cls, collection: str, data: Dict[str, Any]) -> str:
        db = cls._connect()
        data["created_at"] = datetime.utcnow()
        result = db[collection].insert_one(data)
        return str(result.inserted_id)

    @classmethod
    def find_one(cls, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = cls._connect()
        result = db[collection].find_one(query)
        if result:
            result["_id"] = str(result["_id"])
        return result

    @classmethod
    def find_many(cls, collection: str, query: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        db = cls._connect()
        cursor = db[collection].find(query).limit(limit)
        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @classmethod
    def update_one(cls, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        db = cls._connect()
        update_data["updated_at"] = datetime.utcnow()
        result = db[collection].update_one(query, {"$set": update_data})
        return result.modified_count > 0

    @classmethod
    def delete_one(cls, collection: str, query: Dict[str, Any]) -> bool:
        db = cls._connect()
        result = db[collection].delete_one(query)
        return result.deleted_count > 0
