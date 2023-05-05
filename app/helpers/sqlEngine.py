from sqlalchemy import create_engine
from app.constants.db import connectionString

engine = create_engine(connectionString, echo=False)
