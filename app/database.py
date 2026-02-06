from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()
engine = None
SessionLocal = None

def get_engine():
    global engine, SessionLocal

    if engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not set")

        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

    return engine

def get_db():
    get_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
