# app/utils/record_validation.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.sql_models import MedicalRecord

def validate_record_uuid(db: Session, record_uuid: str, patient_id: int):
    """
    Ensures a record_uuid exists AND belongs to the given patient_id.
    Raises HTTPException if validation fails.
    """
    record = (
        db.query(MedicalRecord)
        .filter(
            MedicalRecord.record_uuid == record_uuid,
            MedicalRecord.patient_id == patient_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=400,
            detail="Invalid record_uuid: it does not belong to this patient."
        )

    return record
