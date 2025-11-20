from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import MedicalRecord, Patient
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordRead, MedicalRecordUpdate

router = APIRouter(prefix="/medical_records", tags=["medical_records"])

@router.post("/", response_model=MedicalRecordRead)
def create_record(payload: MedicalRecordCreate, db: Session = Depends(get_db)):
    # check patient exists
    if not db.query(Patient).filter(Patient.patient_id == payload.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")

    record = MedicalRecord(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/{record_id}", response_model=MedicalRecordRead)
def get_record(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec

@router.get("/", response_model=list[MedicalRecordRead])
def list_records(patient_id: int = None, db: Session = Depends(get_db)):
    q = db.query(MedicalRecord)
    if patient_id:
        q = q.filter(MedicalRecord.patient_id == patient_id)
    return q.all()

@router.put("/{record_id}", response_model=MedicalRecordRead)
def update_record(record_id: int, payload: MedicalRecordUpdate, db: Session = Depends(get_db)):
    rec = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(rec, k, v)
    db.commit()
    db.refresh(rec)
    return rec

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(rec)
    db.commit()
    return {"detail": "deleted"}
