# Email Signal Pipeline

A FastAPI service that ingests email metadata, enriches it with mock security signals, and serves them via REST endpoints.

---

## 1. Endpoints

- **POST** `/ingest`  
  - Header: `x-api-key: SuperSecretApiKey123`  
  - Body (JSON):
    ```json
    {
      "sender": "user@example.com",
      "subject": "Test",
      "timestamp": "2025-07-08T12:00:00",
      "links": ["https://example.com/path"]
    }
    ```
  - Returns saved record with `id`.
- **GET** `/signals`  
  - No auth.  
  - Returns list of processed signals:
    ```json
    [
      {
        "raw_id": 1,
        "domain_reputation": "good",
        "url_entropy": 3.46,
        "spoof_check": true
      },
      ...
    ]
    ```

---

## 2. Tech Stack

- **Language & Framework:** Python 3.11, FastAPI  
- **ORM:** SQLAlchemy  
- **DB:** MySQL 8.0 (via Docker)  
- **Containerization:** Docker, Docker Compose  
- **Auth:** API‑key (header)  
- **Validation:** Pydantic v2 models  
- **Background Jobs:** FastAPI BackgroundTasks  

---

## 3. Run with Docker

```bash
git clone https://github.com/Theatharv31/Email-pipeline.git
cd Email-pipeline

# Build & start
docker-compose up --build

# Service running:
# - MySQL on localhost:3308
# - FastAPI on localhost:8000
# Swagger UI: http://localhost:8000/docs

To stop 
docker-compose down

4. Run Locally (without Docker)
Create & activate virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
Prepare database

Start a local MySQL instance (or configure an existing one).

Create .env file in project root:

env
Copy
Edit
DB_HOST=localhost
DB_USER=es_user
DB_PASS=Atharv_test
DB_NAME=email_signals
API_KEY=SuperSecretApiKey123
Run migrations & tables
Tables will auto-create on startup via SQLAlchemy’s Base.metadata.create_all().

Start FastAPI

bash
Copy
Edit
uvicorn api:app --reload --host 0.0.0.0 --port 8000
Access docs
http://localhost:8000/docs

5. File Structure
bash
Copy
Edit
.
├── api.py             # FastAPI app, endpoints, auth, startup logic
├── db.py              # Loads .env, sets up engine, SessionLocal, Base
├── models.py          # ORM models: EmailRaw, EmailSignal
├── processing.py      # Pydantic schemas + process_signals business logic
├── requirements.txt   # Python dependencies (incl. cryptography)
├── Dockerfile         # Python 3.11 image, installs deps, runs Uvicorn
├── docker-compose.yml # Defines MySQL & app services with healthcheck
└── README.md          # This documentation
6. File Responsibilities & Logic
api.py

Defines app = FastAPI(...)

/ingest: stores raw email, triggers BackgroundTasks

/signals: returns enriched data

db.py

Uses python-dotenv to load DB credentials

Creates SQLAlchemy engine, SessionLocal, and Base

models.py

EmailRaw: raw email metadata table

EmailSignal: processed security signals table

processing.py

Schemas: EmailIn, EmailOut (Pydantic)

Logic: process_signals(db, raw)

Mock domain reputation lookup

URL path entropy calculation

Simple spoof check

Saves results to email_signals table

Dockerfile & docker-compose.yml

Containerize app & MySQL

Healthcheck ensures DB readiness before app startup

7. API Security & Scalability
Security

API‑key header (x-api-key) for /ingest

Pydantic validation prevents malformed input

Further enhancements: HTTPS/TLS, rate‑limiting (e.g. Kong), OAuth2/JWT

Scalability

Stateless FastAPI can scale horizontally behind a load balancer

BackgroundTasks can migrate to Celery/Redis or Temporal for robust orchestration

Database can be managed by RDS/Aurora or sharded for high availability
