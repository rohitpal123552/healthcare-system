from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    gender: str
    phone: str
    email: Optional[EmailStr]
    address: Optional[str]

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientRead(PatientBase):
    patient_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
