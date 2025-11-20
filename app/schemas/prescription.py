from pydantic import BaseModel
from typing import Optional

class PrescriptionBase(BaseModel):
    appointment_id: int
    medication: str
    dosage: Optional[str]
    instructions: Optional[str]

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionRead(PrescriptionBase):
    prescription_id: int
    class Config:
        orm_mode = True
