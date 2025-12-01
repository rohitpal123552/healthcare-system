from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImagingCreate(BaseModel):
    patient_id: int
    type: str
    meta: Optional[dict]
    path: str

class ImagingRead(ImagingCreate):
    _id: Optional[str]
    created_at: datetime
