from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

from app.models.Base import Base
from app.models.Account import Account
from app.models.Transaction import TransactionFinal, Transaction
from app.models.Load import Load
from app.constants.db import connectionString
from app.helpers.sqlEngine import engine

def getTables(engine):
    df = pd.read_sql(sql=text("select * from Accounts"), con=engine.connect())   
    return df

Base.metadata.create_all(bind=engine, checkfirst=True)
