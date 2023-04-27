from sqlalchemy import create_engine, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.constants.db import connectionString

engine = create_engine(connectionString, echo=False)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    accountNumber = Column(String)

    # checking account fields 8115
    details = Column(String)
    
    type = Column(String)
    balance = Column(Float)
    checkOrSlipNumber = Column(String)

    # credit account fields
    transactionDate = Column(Date)
    category = Column(String)
    memo = Column(String)

    # shared fields
    postDate = Column(Date) # labeled 'Posting Date' on the checking account -- orm-sqlite doesn't have date types?
    description = Column(String)
    amount = Column(Float)

    # added fields
    sha256 = Column(String)
    observations = Column(Integer)
    firstLoadID = Column(Integer)
    lastLoadID = Column(Integer)

Base.metadata.create_all(bind=engine, checkfirst=True)

class TransactionStaging(Transaction):
    __tablename__ = 'transactions_staging'
