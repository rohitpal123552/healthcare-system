# app/schemas/appointment.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_ts: datetime
    reason: str
    status: Optional[str] = 'scheduled'

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_ts: Optional[datetime]
    reason: Optional[str]
    status: Optional[str]

class AppointmentRead(AppointmentBase):
    appointment_id: int
    created_at: datetime

    class Config:
        orm_mode = True