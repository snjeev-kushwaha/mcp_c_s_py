from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB_NAME

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=3000
        )
    return _client[MONGO_DB_NAME]
