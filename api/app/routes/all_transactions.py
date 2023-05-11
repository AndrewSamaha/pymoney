from fastapi import APIRouter
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.models.Base import Base
from app.models.Account import Account
from app.models.Transaction import TransactionFinal, Transaction
from app.models.Load import Load
from app.constants.db import connectionString

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/transactions")
async def get_users():
    # Create a session and execute the query
    session = Session()
    users = session.query(User).all()
    session.close()
    # Return the results as JSON
    return {"message": "this is all transactions"}
    #{'users': [{'id': user.id, 'name': user.name} for user in users]}