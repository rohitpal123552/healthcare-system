# app/schemas/medical_record.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalRecordBase(BaseModel):
    patient_id: int
    appointment_id: int
    doctor_id: int
    title: str
    summary: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass  # client should not provide record_uuid it'll generate automatic during new medical record

class MedicalRecordUpdate(BaseModel):
    title: Optional[str]
    summary: Optional[str]

class MedicalRecordRead(MedicalRecordBase):
    record_id: int
    record_uuid: str
    created_at: datetime

    class Config:
        orm_mode = True
