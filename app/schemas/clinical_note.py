from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class Observation(BaseModel):
    type: str
    value: str
    ts: Optional[datetime]

class Attachment(BaseModel):
    type: str
    path: str
    caption: Optional[str]

class ClinicalNoteCreate(BaseModel):
    record_uuid: str
    patient_id: int
    doctor_id: int
    note_text: str
    observations: Optional[List[Observation]] = []
    attachments: Optional[List[Attachment]] = []

class ClinicalNoteRead(ClinicalNoteCreate):
    _id: Optional[str]
    created_at: datetime
