from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float, ForeignKey
from db import Base
import datetime


class EmailRaw(Base):
    __tablename__ = "email_raw"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(256), nullable=False)
    subject = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    links = Column(JSON, default=[])


class EmailSignal(Base):
    __tablename__ = "email_signals"
    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("email_raw.id"), nullable=False)
    domain_reputation = Column(String(50))
    url_entropy = Column(Float)
    spoof_check = Column(Boolean)
