from fastapi import APIRouter, HTTPException
from app.database.mongo import mongo_db
from bson import ObjectId
from app.schemas.imaging import ImagingCreate, ImagingRead
from datetime import datetime
from typing import List

router = APIRouter(prefix="/imaging", tags=["imaging"])

@router.post("/", response_model=ImagingRead)
def create_image(payload: ImagingCreate):
    coll = mongo_db.imaging
    doc = payload.dict()
    doc["created_at"] = datetime.utcnow()
    res = coll.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc

@router.get("/{image_id}", response_model=ImagingRead)
def get_image(image_id: str):
    coll = mongo_db.imaging
    doc = coll.find_one({"_id": ObjectId(image_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Image not found")
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/", response_model=List[ImagingRead])
def list_images(patient_id: int = None, limit: int = 50):
    coll = mongo_db.imaging
    q = {}
    if patient_id:
        q["patient_id"] = patient_id
    docs = list(coll.find(q).sort("created_at", -1).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@router.delete("/{image_id}")
def delete_image(image_id: str):
    coll = mongo_db.imaging
    res = coll.delete_one({"_id": ObjectId(image_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"detail": "deleted"}
