# app/schemas/prescription.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrescriptionBase(BaseModel):
    record_id: int
    medication: str
    dosage: Optional[str] = None
    instructions: Optional[str] = None
class PrescriptionCreate(PrescriptionBase):
    pass
class PrescriptionRead(PrescriptionBase):
    prescription_id: int
    issued_at: datetime
    class Config:
        orm_mode = True
