from fastapi import APIRouter, HTTPException
from app.database.mongo import mongo_db
from app.schemas.clinical_note import ClinicalNoteCreate, ClinicalNoteRead
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/clinical_notes", tags=["clinical_notes"])

@router.post("/", response_model=ClinicalNoteRead)
def create_note(payload: ClinicalNoteCreate):
    coll = mongo_db.clinical_notes
    doc = payload.dict()
    doc['created_at'] = datetime.utcnow()
    res = coll.insert_one(doc)
    doc['_id'] = str(res.inserted_id)
    return doc

@router.get("/{note_id}", response_model=ClinicalNoteRead)
def get_note(note_id: str):
    coll = mongo_db.clinical_notes
    doc = coll.find_one({"_id": ObjectId(note_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    doc['_id'] = str(doc['_id'])
    return doc

@router.get("/", response_model=list[ClinicalNoteRead])
def list_notes(patient_id: int = None, limit: int = 50):
    coll = mongo_db.clinical_notes
    q = {}
    if patient_id:
        q['patient_id'] = int(patient_id)
    docs = list(coll.find(q).sort("created_at", -1).limit(limit))
    for d in docs:
        d['_id'] = str(d['_id'])
    return docs

@router.delete("/{note_id}")
def delete_note(note_id: str):
    coll = mongo_db.clinical_notes
    res = coll.delete_one({"_id": ObjectId(note_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail":"deleted"}
