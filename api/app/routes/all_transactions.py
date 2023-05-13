from fastapi import APIRouter
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.models.Base import Base
from app.models.Account import Account
from app.models.Transaction import TransactionFinal, Transaction
from app.models.Load import Load
from app.constants.db import connectionString
from app.helpers.dbsession import get_session

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/transactions")
async def get_users():
    engine = create_engine(connectionString)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()
    results = pd.read_sql(sql=text("""
        SELECT
            sha256,
            postDate,
            transactionDate,
            accountId,
            amount,
            description,
            details,
            type,
            category,
            balance,
            checkOrSlipNumber,
            count(*)
        FROM 
            transactions_all
        WHERE
            postDate >= '2023-01-05'
        GROUP BY
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        ORDER BY
            postDate DESC
    """), con=session.connection())
    session.close()

    return results.to_json()

@router.get("/transactions2")
async def get_transactions_two():
    session_list = list(get_session())
    print(len(session_list))
    session = session_list[len(session_list) - 1]
    results = pd.read_sql(sql=text("""
        SELECT
            sha256,
            postDate,
            transactionDate,
            accountId,
            amount,
            description,
            details,
            type,
            category,
            balance,
            checkOrSlipNumber,
            count(*)
        FROM 
            transactions_all
        WHERE
            postDate >= '2023-01-05'
        GROUP BY
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        ORDER BY
            postDate DESC
    """), con=session.connection())
    session.close()
    return results.to_json()

@router.get("/transactions3")
async def get_transactions_three():
    session_list = list(get_session())
    session = session_list[len(session_list) - 1]
    # transactions = session.query(
    #     Transaction.description,
    #     Transaction.postDate,
    #     Transaction.transactionDate
    # ).all()
    transactions = session.query(Transaction).all()
    session.close()
    return {
        'transactions': [{
            'postDate': t.postDate,
            'transactionDate': t.transactionDate,
            'description': t.description
        } for t in transactions]
    }
