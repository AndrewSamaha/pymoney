from sqlalchemy import create_engine
from ..constants import connectionString

engine = create_engine(connectionString, echo=False)
