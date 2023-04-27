# sql alchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.constants.db import connectionString

engine = create_engine(connectionString, echo=False)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    accountNumber = Column(String)
    interestRate = Column(Float)
    statementDate = Column(Date)
    paymentDueDate = Column(Date)
    csvPath = Column(String)

Base.metadata.create_all(bind=engine, checkfirst=True)
