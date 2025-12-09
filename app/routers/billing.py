# app/routers/billing.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Billing, MedicalRecord
from app.schemas.billing import BillingCreate, BillingRead
from typing import List

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/", response_model=BillingRead)
def create_bill(payload: BillingCreate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == payload.record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record (encounter) not found")

    bill = Billing(
        record_id=payload.record_id, 
        amount=payload.amount, 
        paid=payload.paid, 
        method=payload.method
        )
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
def list_bills(record_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Billing)
    if record_id:
        q = q.filter(Billing.record_id == record_id)
    return q.all()

@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Billing).filter(Billing.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    db.delete(bill)
    db.commit()
    return {"detail": "deleted"}
