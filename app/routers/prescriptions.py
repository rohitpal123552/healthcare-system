# app/routers/prescriptions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Prescription, MedicalRecord
from app.schemas.prescription import PrescriptionCreate, PrescriptionRead
from typing import List

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

@router.post("/", response_model=PrescriptionRead)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == payload.record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record (encounter) not found")

    pr = Prescription(
        record_id=payload.record_id, 
        medication=payload.medication,
        dosage=payload.dosage, 
        instructions=payload.instructions
        )
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return pr

@router.get("/{prescription_id}", response_model=PrescriptionRead)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pr = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pr

@router.get("/", response_model=List[PrescriptionRead])
def list_prescriptions(appointment_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Prescription)
    if appointment_id:
        q = q.filter(Prescription.appointment_id == appointment_id)
    return q.all()

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pr = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(pr)
    db.commit()
    return {"detail": "deleted"}