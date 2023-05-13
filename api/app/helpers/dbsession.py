# database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.Base import Base
from app.constants.db import connectionString

engine = create_engine(connectionString)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()