from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Numeric, Boolean, func
from sqlalchemy.orm import relationship
from app.database.postgres import Base
import sqlalchemy as sa

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(20))
    phone = Column(String(30))
    email = Column(String(150), index=True)
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    medical_records = relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")

class Doctor(Base):
    __tablename__ = 'doctors'
    doctor_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialty = Column(String(100))
    phone = Column(String(30))
    email = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())

    appointments = relationship("Appointment", back_populates="doctor")

class Appointment(Base):
    __tablename__ = 'appointments'
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id'))
    appointment_ts = Column(DateTime, nullable=False)
    reason = Column(Text)
    status = Column(String(20), default='scheduled')
    created_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    prescriptions = relationship("Prescription", back_populates="appointment", cascade="all, delete-orphan")
    billing = relationship("Billing", back_populates="appointment", cascade="all, delete-orphan")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    record_uuid = Column(String(36), nullable=False, unique=True)
    title = Column(String(255))
    summary = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient", back_populates="medical_records")

class Prescription(Base):
    __tablename__ = 'prescriptions'
    prescription_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id', ondelete='CASCADE'), nullable=False)
    medication = Column(Text, nullable=False)
    dosage = Column(Text)
    instructions = Column(Text)
    issued_at = Column(DateTime, server_default=func.now())

    appointment = relationship("Appointment", back_populates="prescriptions")

class Billing(Base):
    __tablename__ = 'billing'
    bill_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id', ondelete='CASCADE'), nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    paid = Column(Boolean, default=False)
    method = Column(String(50))
    billed_at = Column(DateTime, server_default=func.now())

    appointment = relationship("Appointment", back_populates="billing")
