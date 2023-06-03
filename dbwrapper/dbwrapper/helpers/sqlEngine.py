from sqlalchemy import create_engine
from dbwrapper.constants.db import connectionString

engine = create_engine(connectionString, echo=False)
