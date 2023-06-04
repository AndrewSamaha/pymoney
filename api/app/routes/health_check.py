from fastapi import APIRouter
import pandas as pd
import time
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.dbwrapper import *

from app.helpers.dbsession import get_session


start_time = time.time()

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
router = APIRouter()

@router.get("/health-check")
def ping():
    uptime = time.time() - start_time
    # Convert uptime to a human-readable format
    uptime_str = time.strftime('%H:%M:%S', time.gmtime(uptime))
    session = Session()

    return {
        "healthy": "true",
        "uptime": uptime_str,
        "dbStatus": "?"
        }