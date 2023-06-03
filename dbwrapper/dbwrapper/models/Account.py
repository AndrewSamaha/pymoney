# sql alchemy
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from dbwrapper.models.Base import Base

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
