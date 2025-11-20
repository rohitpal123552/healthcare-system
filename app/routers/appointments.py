from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Appointment, Patient, Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentRead)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    # check patient and doctor exist
    if not db.query(Patient).filter(Patient.patient_id == payload.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    if not db.query(Doctor).filter(Doctor.doctor_id == payload.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor not found")

    appt = Appointment(**payload.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.get("/", response_model=list[AppointmentRead])
def list_appointments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Appointment).offset(skip).limit(limit).all()

@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(appointment_id: int, payload: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(appt, k, v)

    db.commit()
    db.refresh(appt)
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"detail": "deleted"}
