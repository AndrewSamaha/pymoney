from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


def truncate_all(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.connection().execute(text("DELETE FROM loads"))
    session.connection().execute(text("DELETE FROM transactions_final"))
    session.connection().execute(text("DELETE FROM transactions_all"))
    session.connection().commit()
    session.close()
