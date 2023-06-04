from sqlalchemy.orm import sessionmaker

#from dbwrapper.main import TransactionFinal

# from dbwrapper import TransactionFinal
# from dbwrapper.helpers.readCsv import openOneCsv, getAccountHistory, setDateColumns
# from dbwrapper.crud.delete.truncate_all import truncate_all
# from dbwrapper.crud.read.select_accounts_df import select_accounts_df
# from dbwrapper.crud.read.select_unique_staged_transactions import select_unique_staged_transactions
# from dbwrapper.crud.create.insert_query_into_table import insert_query_into_table


from ..models import TransactionFinal
from ..helpers.readCsv import openOneCsv, getAccountHistory, setDateColumns

from ..crud.delete.truncate_all import truncate_all
from ..crud.read.select_accounts_df import select_accounts_df
from ..crud.read.select_unique_staged_transactions import select_unique_staged_transactions
from ..crud.create.insert_query_into_table import insert_query_into_table

def full_load_from_csv(engine):
    # truncate all
    truncate_all(engine)

    # Load transactions_all from csv
    accounts = select_accounts_df(engine)
    for index, account in accounts.iterrows():
        path = account['csvPath']
        Session = sessionmaker(bind=engine)
        session = Session()
        allFiles = getAccountHistory(path, account['id'], session)
        # display(allFiles)
        allFiles.to_sql('transactions_all', con=session.connection(), if_exists='append', index=False, chunksize=10)
        session.connection().commit()
        session.close()
    
    # Select transactions_all into transactions_final
    query = select_unique_staged_transactions(engine)
    insert_query_into_table(engine, query, TransactionFinal)