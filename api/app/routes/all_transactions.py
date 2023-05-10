from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.models.data_pipeline_models.Base import Base
from app.models.data_pipeline_models.Account import Account
from app.models.data_pipeline_models.Transaction import TransactionFinal, Transaction
from app.models.data_pipeline_models.Load import Load
from app.constants.db import connectionString

app = FastAPI()
engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
Base = declarative_base()

@app.get('/transactions/all')
async def get_users():
    # Create a session and execute the query
    session = Session()
    users = session.query(User).all()
    session.close()
    # Return the results as JSON
    return "this is all transactions"
    #{'users': [{'id': user.id, 'name': user.name} for user in users]}