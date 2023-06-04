from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from ...helpers import rawQueryDf

def select_summary_df(engine):
    QUERY = """
        SELECT
            COUNT(*) AS total_records,
            MAX(tall.postDate) AS newest_post,
            MIN(tall.postDate) AS oldest_post,
            MAX(tall.transactionDate) AS newest_transaction,
            MIN(tall.transactionDate) AS oldest_transaction
        FROM transactions_final AS tfinal
            JOIN transactions_all AS tall ON tfinal.id = tall.id;
    """
    
    df = rawQueryDf(QUERY, engine)
    return df
