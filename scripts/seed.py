from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import path
import sys
import os
from dotenv import load_dotenv

# directory reach/ this lets us load modules from ../app
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

 
#from ..dbwrapper.dbwrapper.models import Account # app.models.Account import Account
#from app.models.Transaction import Transaction
#from app.models.Load import Load
from app.constants.db import connectionString

print("loading dotenv()")

load_dotenv()

print("line 22")

def seed(feedFolder):
    seedFolder = 'db/seed_data/'
    print("running seed()")
    engine = create_engine(connectionString, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

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

if __name__ == "__main__":
    print('the seed as being run as a main package')
    project_level = os.environ.get("PROJECT_LEVEL")
    dblevel = os.environ.get("DBWRAPPER")
    print(f"project_level={project_level}")
    print(f"dblevel={dblevel}")
else:
    print('the seed is being imported')
