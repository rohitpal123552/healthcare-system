from pydantic import BaseModel
from typing import Optional

class BillingBase(BaseModel):
    appointment_id: int
    amount: float
    paid: Optional[bool] = False
    method: Optional[str]

class BillingCreate(BillingBase):
    pass

class BillingRead(BillingBase):
    bill_id: int
    class Config:
        orm_mode = True
