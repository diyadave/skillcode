# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()
_engine = None
_SessionLocal = None

def get_engine():
    global _engine, _SessionLocal

    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return None  # ← IMPORTANT: do NOT crash

        _engine = create_engine(database_url, pool_pre_ping=True)
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine
        )

    return _engine

def get_db():
    engine = get_engine()
    if engine is None:
        raise RuntimeError("Database not initialized")

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
