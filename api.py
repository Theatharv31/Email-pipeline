from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import schemas
import models
import processing
import logging
from db import SessionLocal, engine, Base
logging.basicConfig(level=logging.INFO)
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Email Signal Pipeline")

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Simple API key auth
API_KEY = "SuperSecretApiKey123"


def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.post("/ingest", response_model=schemas.EmailOut, dependencies=[Depends(api_key_auth)])
def ingest_email(
    payload: schemas.EmailIn,
    background: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logging.info(f"Received email from: {payload.sender}")
    # Save raw record
    raw = models.EmailRaw(**payload.dict())
    raw.links = [str(link) for link in raw.links]  # Convert HttpUrl to str
    db.add(raw)
    db.commit()
    db.refresh(raw)

    # Trigger background processing
    background.add_task(processing.process_signals, db, raw)
    return raw

# route to get all signals


@app.get("/signals")
def get_signals(db: Session = Depends(get_db)):
    signals = db.query(models.EmailSignal).all()
    return JSONResponse(content=[{
        "raw_id": s.raw_id,
        "domain_reputation": s.domain_reputation,
        "url_entropy": s.url_entropy,
        "spoof_check": s.spoof_check
    } for s in signals])
