from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Billing, Appointment
from app.schemas.billing import BillingCreate, BillingRead
from typing import List

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/", response_model=BillingRead)
def create_bill(payload: BillingCreate, db: Session = Depends(get_db)):
    if not db.query(Appointment).filter(Appointment.appointment_id == payload.appointment_id).first():
        raise HTTPException(status_code=404, detail="Appointment not found")

    bill = Billing(**payload.dict())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

@router.get("/{bill_id}", response_model=BillingRead)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Billing).filter(Billing.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@router.get("/", response_model=List[BillingRead])
def list_bills(appointment_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Billing)
    if appointment_id:
        q = q.filter(Billing.appointment_id == appointment_id)
    return q.all()

@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Billing).filter(Billing.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    db.delete(bill)
    db.commit()
    return {"detail": "deleted"}
