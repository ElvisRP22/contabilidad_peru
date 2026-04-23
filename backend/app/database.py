from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    SQLModel.metadata.create_all(bind=engine)