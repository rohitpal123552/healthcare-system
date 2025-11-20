from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Prescription, Appointment
from app.schemas.prescription import PrescriptionCreate, PrescriptionRead

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

@router.post("/", response_model=PrescriptionRead)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    if not db.query(Appointment).filter(Appointment.appointment_id == payload.appointment_id).first():
        raise HTTPException(status_code=404, detail="Appointment not found")

    pr = Prescription(**payload.dict())
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

@router.get("/", response_model=list[PrescriptionRead])
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
