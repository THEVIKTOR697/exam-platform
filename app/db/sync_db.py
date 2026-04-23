# app/db/sync_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
print("SYNCURL:", SYNC_DATABASE_URL)

if not SYNC_DATABASE_URL:
    raise ValueError("SYNC_DATABASE_URL is not set")

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        print("Engine NONE, Creating engine...")
        _engine = create_engine(
            SYNC_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_timeout=30,
            pool_size=5,
            max_overflow=10
        )
    return _engine

def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()