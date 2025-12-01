from pymongo import MongoClient
from app.core.config import settings

MONGO_URI = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}"
client = MongoClient(MONGO_URI)
mongo_db = client[settings.MONGO_DB]

def init_mongo():
    # Create collections if not exist
    if "clinical_notes" not in mongo_db.list_collection_names():
        mongo_db.create_collection("clinical_notes")
        mongo_db.clinical_notes.create_index("record_uuid")
        mongo_db.clinical_notes.create_index("patient_id")
        mongo_db.clinical_notes.create_index("doctor_id")

    if "imaging" not in mongo_db.list_collection_names():
        mongo_db.create_collection("imaging")
        mongo_db.imaging.create_index("patient_id")
        mongo_db.imaging.create_index("type")

    print("MongoDB collection initialized.")
    
