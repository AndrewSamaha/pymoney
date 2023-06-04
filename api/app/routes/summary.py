from fastapi import APIRouter
import pandas as pd
import time
import json
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.dbwrapper import *

from app.helpers.dbsession import get_session


start_time = time.time()

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
router = APIRouter()

@router.get("/summary")
def summary():
    df = select_summary_df(engine)
    return  json.loads(df.to_json())