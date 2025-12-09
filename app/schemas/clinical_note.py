# app/schemas/clinical_note.pyf
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Observation(BaseModel):
    type: str
    value: str
    ts: Optional[datetime]

class Attachment(BaseModel):
    file_name: str
    file_url: str
    caption: Optional[str]

class ClinicalNoteCreate(BaseModel):
    record_uuid: str
    patient_id: int
    doctor_id: int
    note_text: str
    observations: Optional[Dict[str, Any]] = {}
    attachments: Optional[List[Attachment]] = []

class ClinicalNoteRead(ClinicalNoteCreate):
    _id: Optional[str]
    record_uuid: str
    created_at: datetime
