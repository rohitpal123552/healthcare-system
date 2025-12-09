from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialty: str
    phone: str
    email: Optional[EmailStr]

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class DoctorRead(DoctorBase):
    doctor_id: int
    class Config:
        orm_mode = True
