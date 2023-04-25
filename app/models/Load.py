# sql alchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.constants.db import connectionString

engine = create_engine(connectionString, echo=False)
Base = declarative_base()

class Load(Base):
    __tablename__ = 'loads'
    id = Column(Integer, primary_key=True)
    accountId = Column(Integer)
    fullFilePath = Column(String)
    dateTime = Column(DateTime)

Base.metadata.create_all(bind=engine, checkfirst=True)
