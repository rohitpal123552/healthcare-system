from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.postgres import get_db
from app.models import sql_models
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientRead)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = sql_models.Patient(**payload.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(sql_models.Patient).filter(sql_models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/", response_model=List[PatientRead])
def list_patients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    patients = db.query(sql_models.Patient).offset(skip).limit(limit).all()
    return patients

@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(sql_models.Patient).filter(sql_models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(patient, k, v)
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(sql_models.Patient).filter(sql_models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Capture name before deletion
    patient_name = f"{patient.first_name} {patient.last_name}"

    db.delete(patient)
    db.commit()
    return {"detail": f"Patient '{patient_name}' deleted successfully"}
