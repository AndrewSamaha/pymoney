# sql alchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.constants.db import connectionString
from app.models.Base import Base
from app.helpers.sqlEngine import engine

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    accountNumber = Column(String)
    interestRate = Column(Float)
    statementDate = Column(Date)
    paymentDueDate = Column(Date)
    csvPath = Column(String)

    loads = relationship("Load", back_populates="account")
