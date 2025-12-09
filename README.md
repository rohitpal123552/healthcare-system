# Healthcare Management System

**Hybrid SQL + NoSQL Database Project (FastAPI + PostgreSQL + MongoDB)**

---

## Overview

This project is a **Healthcare Management System** designed using a **hybrid database architecture**:

* **PostgreSQL (SQL)** for structured and relational healthcare data
* **MongoDB (NoSQL)** for unstructured clinical notes, observations, and attachments
* **FastAPI** backend providing complete CRUD functionality
* Fully compliant with project requirements:
  ✔ SQL ER diagrams
  ✔ NoSQL JSON document schemas
  ✔ CRUD + aggregation queries
  ✔ 100+ records per table
  ✔ Professional documentation

---

## Features

### **1. SQL (PostgreSQL) Models**

| Table             | Description                     |
| ----------------- | ------------------------------- |
| `patients`        | Patient demographic data        |
| `doctors`         | Doctors directory               |
| `appointments`    | Appointment scheduling          |
| `medical_records` | Encounter-based EMR (with UUID) |
| `prescriptions`   | Medicines linked to encounters  |
| `billing`         | Billing & payment information   |

### **2. NoSQL (MongoDB) Collections**

| Collection       | Description                                      |
| ---------------- | ------------------------------------------------ |
| `clinical_notes` | Doctor's notes, observations, file attachments   |

---

## ER Diagrams

### **SQL ER Diagram**

👉 Stored in `/docs/sql_erd.png`

### **MongoDB Document Structure Diagram**

👉 Stored in `/docs/mongodb_schema.png`

### **Combined Hybrid Architecture Diagram**

👉 Stored in `/docs/sql_and_nosql.png`

---

## Database Schema Summary

### **PostgreSQL (SQL)**

Follows strict relational design with foreign keys:

* 1 patient → many appointments
* 1 appointment → 1 medical record (encounter)
* 1 record → many prescriptions / billing entries
* UUID generated automatically for encounter management

### **MongoDB (NoSQL)**

Used for:

* Free-text notes
* Observations (BP, temperature, symptoms, etc.)
* Dynamic JSON objects
* Attachments
* Non-relational encounter enrichment

---

## Project Structure

```
app/
│── main.py
├── core/config.py
│── database/
│     ├── postgres.py
│     ├── mongo.py
│── models/
│     ├── sql_models.py
│── routers/
│     ├── patients.py
│     ├── doctors.py
│     ├── appointments.py
│     ├── medical_records.py
│     ├── prescriptions.py
│     ├── billing.py
│     ├── clinical_notes.py
│── schemas/
│     ├── patients.py
│     ├── doctors.py
│     ├── appointments.py
│     ├── medical_records.py
│     ├── prescriptions.py
│     ├── billing.py
│     ├── clinical_notes.py
│── utils/
│     ├── validators.py   (validate_record_uuid)
│── tests/
│     ├── test_patients.py
│     ├── test_medical_records.py
│     ├── test_clinical_notes.py
docs/
│  ├── sql_erd.png
│  ├── nosql_erd.png
│  ├── sql_and_nosql_erd.png
docker-compose.yml
requirements.txt
.env
README.md
```

---

# Installation & Setup

## **1. Clone Repository**

```bash
git clone https://github.com/yourname/healthcare-system.git
cd healthcare-system
```

## Running the Project with Docker

## **2. Start PostgreSQL + MongoDB
```bash
docker-compose up -d
```

Postgres → http://localhost:5432
MongoDB → http://localhost:27017
pgAdmin → http://localhost:8080
mongo-express → http://localhost:8081

## **3. Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

## **4. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

# Running the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at:

👉 **Swagger UI:**
[http://localhost:8000/docs](http://localhost:8000/docs)

👉 **Redoc:**
[http://localhost:8000/redoc](http://localhost:8000/redoc)

Postgres → http://localhost:5432
MongoDB → http://localhost:27017
pgAdmin → http://localhost:8080
mongo-express → http://localhost:8081

---

# API Overview (CRUD + Validations)

## **1. Patients**

```
POST /patients/
GET /patients/{id}
PUT /patients/{id}
DELETE /patients/{id}
```

## **2. Doctors**

```
POST /doctors/
GET /doctors/{id}
PUT /doctors/{id}
DELETE /doctors/{id}
```

## **3. Appointments**

```
POST /appointments/
GET /appointments/{id}
PUT /appointments/{id}
DELETE /appointments/{id}
```

## **4. Medical Records (UUID Auto-Generated)**

```
POST /medical-records/
GET /medical-records/{id}
PUT /medical-records/{id}
DELETE /medical-records/{id}
```

## **5. Clinical Notes (MongoDB)**

Includes dynamic JSON validation with:

### `validate_record_uuid(record_uuid, patient_id)`

```
POST /clinical-notes/
GET /clinical-notes/{record_uuid}
DELETE /medical-records/{id}
```

## **6. Prescriptions**

```
POST /prescriptions/
GET /prescriptions/{id}
DELETE /prescriptions/{id}
```

## **7. Billing**

```
POST /billing/
GET /billing/{id}
DELETE /billing/{id}
```

---

# Aggregation Queries

### **Example – Count appointments per doctor**

```sql
SELECT doctor_id, COUNT(*)
FROM appointments
GROUP BY doctor_id;
```

### **Example – MongoDB: Symptoms frequency**

```js
db.clinical_notes.aggregate([
  { $unwind: "$observations.symptoms" },
  { $group: { _id: "$observations.symptoms", total: { $sum: 1 } } }
])
```

---

# Testing

## **Run All Tests**

```bash
pytest -v
```

Includes:

* Patient CRUD tests
* Medical record UUID validation
* Clinical notes patient/doctor validation
* record_uuid relational consistency tests

---

# Validation Rules Summary

* Patient must exist before creating appointment
* Doctor must exist before encounter or notes
* `record_uuid` must match the correct patient
* Clinical notes store only if **record_uuid → patient_id match succeeds**

---

# Technologies Used
* Python 3.9.6
* FastAPI
* SQLAlchemy
* PostgreSQL
* MongoDB
* Docker / Docker-Compose
* Pydantic
* Uvicorn

# Conclusion

This project demonstrates:

✔ Hybrid SQL + NoSQL database design
✔ Full CRUD operations
✔ Aggregation queries in SQL & MongoDB
✔ Clean code structured for production
✔ Well-defined ER diagrams & schemas

