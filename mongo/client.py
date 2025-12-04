from pymongo import MongoClient
from ..config.settings import MONGO_URI, MONGO_DB
from ..utils.logger import info, error
from pymongo import MongoClient


_client = None
_db = None


def get_client():
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGO_URI)
            info("Connected to MongoDB")
        except Exception as e:
            error(f"Failed to connect to MongoDB: {e}")
            raise
    return _client


def get_db():
    global _db
    if _db is None:
        client = get_client()

        db_name: str = str(MONGO_DB)

        _db = client[db_name]
        info(f"Using MongoDB database: {db_name}")
    return _db
