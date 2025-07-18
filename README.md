# Email Signal Pipeline

A FastAPI service that ingests email metadata, enriches it with mock security signals, and serves them via REST endpoints.

---

## 1. Endpoints

- _POST_ /ingest

  - _Header:_

    x-api-key: SuperSecretApiKey123

  - _Body (JSON):_
    json
    {
    "sender": "user@example.com",
    "subject": "Test",
    "timestamp": "2025-07-08T12:00:00",
    "links": ["https://example.com/path"]
    }
  - _Response:_  
    Saved record with id and all submitted fields.

- _GET_ /signals
  - No authentication required.
  - _Response:_  
    List of processed signals:
    json
    [
    {
    "raw_id": 1,
    "domain_reputation": "good",
    "url_entropy": 3.46,
    "spoof_check": true
    },
    ...
    ]

---

## 2. Tech Stack

- _Language & Framework:_ Python 3.11, FastAPI
- _ORM:_ SQLAlchemy
- _Database:_ MySQL 8.0 (via Docker)
- _Containerization:_ Docker & Docker Compose
- _Authentication:_ API‑key (header)
- _Validation:_ Pydantic v2 models
- _Background Jobs:_ FastAPI BackgroundTasks

---

## 3. Run with Docker

bash
git clone https://github.com/Theatharv31/Email-pipeline.git
cd Email-pipeline

# Build & start services

docker-compose up --build

# MySQL → localhost:3308

# FastAPI → localhost:8000

# Open Swagger UI:

http://localhost:8000/docs

# To stop and remove containers:

docker-compose down

## 4. Run without Docker

bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Prepare Database

DB*HOST=localhost
DB_USER=es_user
DB_PASS=Atharv*#####
DB_NAME=email_signals
API_KEY=SuperSecretApiKey123

# Run Application

uvicorn api:app --reload --host 0.0.0.0 --port 8000
http://localhost:8000/docs

bash

## File Struture

bash
.
├── api.py # FastAPI app, endpoints, auth, startup logic
├── db.py # Loads .env, sets up engine, SessionLocal, Base
├── models.py # ORM models: EmailRaw, EmailSignal
├── processing.py # Pydantic schemas + "process_signals" logic
├── requirements.txt # Python dependencies (incl. cryptography)
├── Dockerfile # Python image, installs deps, runs Uvicorn
├── docker-compose.yml # Defines MySQL & app services with healthcheck
└── README.md # This documentation

```bash

---

## 6. 📂 File Responsibilities & Logic

### api.py
- Initializes app = FastAPI(...)
- Defines:
  - POST /ingest: Stores raw email metadata, triggers background task
  - GET /signals: Returns enriched email security signals
- Handles API key validation using FastAPI Header
- Uses BackgroundTasks for async processing

### db.py
- Loads DB credentials using python-dotenv
- Sets up:
  - SQLAlchemy engine
  - SessionLocal
  - Declarative Base

### models.py
- *EmailRaw*: stores raw email input (sender, subject, links, timestamp)
- *EmailSignal*: stores computed security signals (domain_reputation, url_entropy, spoof_check)

### processing.py
- *Pydantic Schemas*:
  - EmailIn: Input schema
  - EmailOut: Output schema with id
- *Signal Processing Logic*:
  - Domain reputation lookup from mock table
  - URL path entropy calculation (Shannon entropy)
  - Simple spoof check based on sender domain
  - Writes results into email_signals table

### Dockerfile & docker-compose.yml
- Dockerfile:
  - Based on python:3.11-slim
  - Installs dependencies and runs uvicorn server
- Compose file:
  - Spins up MySQL + API container
  - Uses healthchecks to ensure DB is ready before app starts

---

## 7. 🔐 API Security & ⚡ Scalability

### ✅ Security
- Uses x-api-key header for /ingest to restrict access
- Payloads are validated via *Pydantic*
- Can be extended with:
  - *HTTPS/TLS* for encrypted transport
  - *Rate limiting* (e.g., with Kong or Traefik)
  - *OAuth2 / JWT* for token-based authentication

### 🚀 Scalability
- *Stateless API app* – can be scaled horizontally with load balancers
- Background processing can scale by:
  - Migrating to *Celery + Redis*
  - Or using *Temporal* for advanced workflow orchestration
- *Database scaling* options:
  - Migrate to *managed RDS (e.g. AWS/Aurora)*
  - *Sharding* or *read replicas* for performance at scale
```
