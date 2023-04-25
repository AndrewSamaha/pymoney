from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.Load import Load
from app.constants.db import connectionString


engine = create_engine(connectionString, echo=False)


# Base = declarative_base()
# Base.metadata.create_all(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

def getTables(engine):
    df = pd.read_sql(sql=text("select * from Accounts"), con=engine.connect())   
    return df