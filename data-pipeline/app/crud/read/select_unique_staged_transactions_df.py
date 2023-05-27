import pandas as pd

def select_unique_staged_tranactions_df(engine):
    QUERY_FINAL_TRANSACTIONS = """
        SELECT
            sha256,
            postDate,
            transactionDate,
            accountId,
            amount,
            description,
            memo,
            details,
            type,
            category,
            balance,
            checkOrSlipNumber,
            count(*)
        FROM 
            transactions_all
        GROUP BY
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        ORDER BY
            postDate DESC
    """
    return setDateColumns(pd.read_sql(sql=text(QUERY_FINAL_TRANSACTIONS), con=engine.connect()))