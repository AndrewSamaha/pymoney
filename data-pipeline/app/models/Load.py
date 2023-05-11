# sql alchemy
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
from app.models.Base import Base

class Load(Base):
    __tablename__ = 'loads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    accountId = mapped_column(ForeignKey('accounts.id'))
    fullFilePath = Column(String)
    dateTime = Column(DateTime, default=datetime.utcnow)
    account = relationship("Account", back_populates="loads")
