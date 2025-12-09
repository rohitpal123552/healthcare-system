# app/schemas/billing.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BillingBase(BaseModel):
    record_id: int
    amount: float
    paid: Optional[bool] = False
    method: Optional[str] = None

class BillingCreate(BillingBase):
    pass

class BillingRead(BillingBase):
    bill_id: int
    billed_at: datetime

    class Config:
        orm_mode = True
