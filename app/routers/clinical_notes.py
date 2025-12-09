# app/routers/clinical_notes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.mongo import mongo_db
from app.database.postgres import get_db
from app.models.sql_models import Patient, Doctor, MedicalRecord, Appointment
from app.schemas.clinical_note import ClinicalNoteCreate, ClinicalNoteRead
from app.utils.record_validation import validate_record_uuid
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Any


router = APIRouter(prefix="/clinical_notes", tags=["clinical_notes"])

@router.post("/", response_model=ClinicalNoteRead)
def create_clinical_note(payload: ClinicalNoteCreate, db: Session = Depends(get_db)):

    # Validate patient existence
    patient = db.query(Patient).filter(Patient.patient_id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    # Validate doctor existence
    doctor = db.query(Doctor).filter(Doctor.doctor_id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found.")

    # Validate that record_uuid exists AND belongs to this patient
    record = validate_record_uuid(
        db=db,
        record_uuid=payload.record_uuid,
        patient_id=payload.patient_id
    )
    # record = (
    #     db.query(MedicalRecord)
    #     .filter(
    #         MedicalRecord.record_uuid == payload.record_uuid,
    #         MedicalRecord.patient_id == payload.patient_id
    #     )
    #     .first()
    # )

    # if not record:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Invalid record_uuid: It does not belong to this patient."
    #     )

    # Prepare Mongo document
    note_doc: Dict[str, Any] = {
        "record_uuid": payload.record_uuid,
        "patient_id": payload.patient_id,
        "doctor_id": payload.doctor_id,
        "note_text": payload.note_text,
        "observations": payload.observations or {},
        "attachments": [a.dict() for a in (payload.attachments or [])],
        "created_at": datetime.utcnow()
    }

    # Insert into MongoDB
    notes_collection = mongo_db["clinical_notes"]
    result = notes_collection.insert_one(note_doc)

    # Format response
    note_doc["_id"] = str(result.inserted_id)
    return note_doc

@router.get("/{note_id}", response_model=ClinicalNoteRead)
def get_note(note_id: str):
    coll = mongo_db.clinical_notes
    doc = coll.find_one({"_id": ObjectId(note_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    doc['_id'] = str(doc['_id'])
    return doc

@router.get("/", response_model=List[ClinicalNoteRead])
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