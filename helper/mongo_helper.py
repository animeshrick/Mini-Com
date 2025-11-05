from dotenv import load_dotenv
import os
import certifi
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.database import Database
import logging


class MongoHelper:
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    load_dotenv()

    @classmethod
    def _connect(cls) -> Optional[Database]:
        """Synchronous MongoDB connection using PyMongo (Render-safe)."""
        if cls._client is None:
            mongo_uri = os.getenv("MONGODB_URI")
            print(f"mongo_uri == {mongo_uri}")
            if not mongo_uri:
                raise RuntimeError("MONGODB_URI not found in environment variables")

            try:
                cls._client = MongoClient(
                    mongo_uri,
                    tls=True,
                    tlsCAFile=certifi.where(),
                    serverSelectionTimeoutMS=30000,  # Increased timeout
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000
                )

                # Test the connection
                cls._client.admin.command("ping")

                db_name = os.getenv("MONGO_DB_NAME", "Dukan")
                cls._db = cls._client[db_name]
                print(f"✅ Connected to MongoDB database: {db_name}")

            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                logging.error(f"MongoDB connection failed: {e}")
                cls._client = None
                cls._db = None

        return cls._db

    @classmethod
    def _ensure_connection(cls) -> Database:
        """Ensures database connection is available."""
        db = cls._connect()
        if db is None:
            raise RuntimeError("⚠️ MongoDB connection not available")
        return db

    # -------------------------
    # CRUD
    # -------------------------
    @classmethod
    def insert_one(cls, collection: str, data: Dict[str, Any]) -> Optional[str]:
        try:
            db = cls._ensure_connection()
            data["created_at"] = datetime.utcnow()
            result = db[collection].insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logging.error(f"⚠️ Failed to insert into {collection}: {e}")
            return None

    @classmethod
    def find_one(cls, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            db = cls._ensure_connection()
            result = db[collection].find_one(query)
            if result:
                result["_id"] = str(result["_id"])
            return result
        except Exception as e:
            logging.error(f"⚠️ Failed to find_one in {collection}: {e}")
            return None

    @classmethod
    def find_many(cls, collection: str, query: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        try:
            db = cls._ensure_connection()
            cursor = db[collection].find(query).limit(limit)
            results = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                results.append(doc)
            return results
        except Exception as e:
            logging.error(f"⚠️ Failed to find_many in {collection}: {e}")
            return []

    @classmethod
    def update_one(cls, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        try:
            db = cls._ensure_connection()
            update_data["updated_at"] = datetime.utcnow()
            result = db[collection].update_one(query, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"⚠️ Failed to update_one in {collection}: {e}")
            return False

    @classmethod
    def delete_one(cls, collection: str, query: Dict[str, Any]) -> bool:
        try:
            db = cls._ensure_connection()
            result = db[collection].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"⚠️ Failed to delete_one in {collection}: {e}")
            return False