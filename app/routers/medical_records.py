# app/routers/medical_records.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import MedicalRecord, Patient, Doctor, Appointment
from app.schemas.medical_records import MedicalRecordCreate, MedicalRecordRead, MedicalRecordUpdate
from typing import List

router = APIRouter(prefix="/medical_records", tags=["medical_records"])

@router.post("/", response_model=MedicalRecordRead)
def create_record(payload: MedicalRecordCreate, db: Session = Depends(get_db)):
    # Validate patient
    patient = db.query(Patient).filter(Patient.patient_id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # validate appointment
    appointment = db.query(Appointment).filter(Appointment.appointment_id == payload.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # # Optional: validate appointment if provided
    # appointment = None
    # if payload.appointment_id:
    #     appointment = db.query(Appointment).filter(Appointment.appointment_id == payload.appointment_id).first()
    #     if not appointment:
    #         raise HTTPException(status_code=404, detail="Appointment not found")

    # validate doctor
    doctor = db.query(Doctor).filter(Doctor.doctor_id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    # # Optional: validate doctor if provided
    # if payload.doctor_id:
    #     doctor = db.query(Doctor).filter(Doctor.doctor_id == payload.doctor_id).first()
    #     if not doctor:
    #         raise HTTPException(status_code=404, detail="Doctor not found")

    record = MedicalRecord(
        patient_id=payload.patient_id,
        appointment_id=payload.appointment_id,
        doctor_id=payload.doctor_id,
        title=payload.title,
        summary=payload.summary
    )
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

@router.get("/", response_model=List[MedicalRecordRead])
def list_records(patient_id: int = None, db: Session = Depends(get_db)):
    q = db.query(MedicalRecord)
    if patient_id:
        q = q.filter(MedicalRecord.patient_id == patient_id)
    return q.order_by(MedicalRecord.created_at.desc()).limit(200).all()

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