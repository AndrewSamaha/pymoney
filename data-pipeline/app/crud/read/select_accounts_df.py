from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pandas as pd

def select_accounts_df(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_sql(sql=text("select * from Accounts"), con=session.connection())   
    session.close()
    return df
