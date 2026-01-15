from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from app.config import MONGO_URI, MONGO_DB_NAME

_client = None

def get_db():
    global _client
    if not _client:
        _client = MongoClient(MONGO_URI)
    return _client[MONGO_DB_NAME]
