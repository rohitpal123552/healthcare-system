from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Doctor
from app.schemas.doctor import DoctorCreate, DoctorRead, DoctorUpdate
from typing import List

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/", response_model=DoctorRead)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**payload.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.get("/", response_model=List[DoctorRead])
def list_doctors(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Doctor).offset(skip).limit(limit).all()

@router.put("/{doctor_id}", response_model=DoctorRead)
def update_doctor(doctor_id: int, payload: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(doctor, k, v)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Capture name before deletion
    doctor_name = f"{doctor.first_name} {doctor.last_name}"
    
    db.delete(doctor)
    db.commit()
    return {"detail": f"Patient '{doctor_name}' deleted successfully"}
