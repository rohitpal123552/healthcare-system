from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MedicalRecordBase(BaseModel):
    patient_id: int
    record_uuid: Optional[str]
    title: Optional[str]
    summary: Optional[str]

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    title: Optional[str]
    summary: Optional[str]

class MedicalRecordRead(MedicalRecordBase):
    record_id: int
    class Config:
        orm_mode = True
