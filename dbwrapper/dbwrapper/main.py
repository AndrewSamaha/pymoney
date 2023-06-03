from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# from dbwrapper.models.Base import Base
# from dbwrapper.models.Account import Account
# from dbwrapper.models.Transaction import TransactionFinal, Transaction
# from dbwrapper.models.Load import Load
# from dbwrapper.constants.db import connectionString
# from dbwrapper.helpers.sqlEngine import engine

from dbwrapper import Base
from dbwrapper.helpers.sqlEngine import engine
#from dbwrapper.models.Account import Account
#from dbwrapper.models.Transaction import TransactionFinal, Transaction
#from dbwrapper.models.Load import Load
# from dbwrapper.constants.db import connectionString
# from dbwrapper.helpers.sqlEngine import engine

def getTables(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_sql(sql=text("select * from Accounts"), con=session.connection())   
    session.close()
    return df

Base.metadata.create_all(bind=engine, checkfirst=True)
