from sqlalchemy import create_engine
from ...constants import mockConnectionString

def createMockEngine(connectionString=mockConnectionString):
    return create_engine(connectionString, echo=False)
