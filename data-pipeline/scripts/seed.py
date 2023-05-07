from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import path
import sys
import os

# directory reach/ this lets us load modules from ../app
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

 
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.Load import Load
from app.constants.db import connectionString


engine = create_engine(connectionString, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

seedFolder = 'db/seed_data/'

for filename in os.listdir(seedFolder):
    filepath = f"{seedFolder}/{filename}"
    print(filepath)
    file = open(filepath, 'r')
    lines = file.readlines()
    conn = engine.connect()

    for seedline in lines:
        print(seedline)
        conn.execute(text(seedline))
        conn.commit()
