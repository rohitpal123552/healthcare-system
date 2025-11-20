from fastapi import FastAPI
from app.routers import patients, doctors, appointments, medical_records, prescriptions, billing, clinical_notes, imaging
from app.seed.seed_router import router as seed_router

app = FastAPI(title="Healthcare Hybrid DB API", version="1.0")

# include routers (ensure import paths are correct)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(prescriptions.router)
app.include_router(billing.router)
app.include_router(clinical_notes.router)
app.include_router(imaging.router)
app.include_router(seed_router)
