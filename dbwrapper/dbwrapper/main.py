from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

from .dbwrapper import Base
from .dbwrapper.helpers.sqlEngine import engine

def getTables(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_sql(sql=text("select * from Accounts"), con=session.connection())   
    session.close()
    return df

Base.metadata.create_all(bind=engine, checkfirst=True)
