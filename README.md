🏥 Healthcare System Management – Hybrid PostgreSQL + MongoDB (FastAPI)

A complete health system management backend using FastAPI, PostgreSQL, and MongoDB to satisfy hybrid database requirements described in the project brief.
This project includes:

✔ Full CRUD for SQL entities
✔ Full CRUD for MongoDB entities
✔ Production-grade folder structure
✔ Docker Compose environments
✔ Postman collection & API test script

---
🚀 Features

SQL (PostgreSQL via SQLAlchemy)
Patients
Doctors
Appointments
Medical Records
Prescriptions
Billing

NoSQL (MongoDB via pymongo)
Clinical Notes
Imaging Documents

Other features 

Modular routers, schemas, models, services
Ready for production container deployment 

---
📁 Project Structure
healthcare-system/
│
├── docker-compose.yml
├── requirements.txt
├── .env
│
└── app/
    ├── main.py
    ├── core/config.py
    ├── database/
    │   ├── postgres.py
    │   └── mongo.py
    ├── models/sql_models.py
    ├── routers/
    │   ├── patients.py
    │   ├── doctors.py
    │   ├── appointments.py
    │   ├── medical_records.py
    │   ├── prescriptions.py
    │   ├── billing.py
    │   ├── clinical_notes.py
    │   └── imaging.py
    ├── schemas/
    │   ├── *.py (Pydantic schemas)

---
🐳 Running the Project with Docker

1. Start PostgreSQL + MongoDB
docker-compose up -d

Postgres → http://localhost:5432
MongoDB → http://localhost:27017
pgAdmin → http://localhost:8080
mongo-express → http://localhost:8081

---
🐍 Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

---
▶️ Run FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Open API docs:
👉 http://localhost:8000/docs

---
📌 Available API Endpoints
PostgreSQL (SQL)
Entity	Endpoints
Patients	GET /patients/, POST /patients/, PUT /patients/{id}, DELETE
Doctors	/doctors/
Appointments	/appointments/
Medical Records	/medical_records/
Prescriptions	/prescriptions/
Billing	/billing/

MongoDB (NoSQL)
Entity	Endpoints
Clinical Notes	/clinical_notes/
Imaging	/imaging/

---
🧪 How to Run Tests
Use the provided:
API Automated Script
Postman Collection
Commands included below.

---
📦 Technologies Used
Python 3.10
FastAPI
SQLAlchemy
PostgreSQL
MongoDB
Docker / Docker-Compose
Pydantic
Uvicorn

---
🙌 Author
Rohit
Hybrid Database Health System Project
