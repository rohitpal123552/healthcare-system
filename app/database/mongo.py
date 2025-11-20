from pymongo import MongoClient
from app.core.config import settings

MONGO_URI = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}"
client = MongoClient(MONGO_URI)
mongo_db = client[settings.MONGO_DB]
