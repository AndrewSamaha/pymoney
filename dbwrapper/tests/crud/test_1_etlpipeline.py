import pytest
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from dbwrapper.constants import getConnectionString, getSeedFolder
from dbwrapper.helpers import seed_worker, getSeedEngine, getAccountHistory, openOneCsv, prepCheckingDf
from dbwrapper.models import Base
from dbwrapper.crud.read import select_accounts_df

rawCsvPath='tests/mock_data/rawTransactionHistory'

class TestEtlPipeline:
    @pytest.fixture(scope='class')
    def sqlite_file(self, tmp_path_factory):
        fn = tmp_path_factory.getbasetemp() / 'mockdb.sqlite'
        return fn

    @pytest.fixture
    def connection(self, sqlite_file):
        ENV = 'Test'
        dryrun = False
        seedFolder = getSeedFolder(ENV)
        connectionString = f"sqlite:///{str(sqlite_file)}"
        engine = getSeedEngine(connectionString)
        return {
            'ENV': ENV,
            'dryrun': dryrun,
            'seedFolder': seedFolder,
            'connectionString': connectionString,
            'engine': engine
        }
    
    @pytest.fixture
    def engine(self, connection):
        return connection['engine']

    def test_create_and_seed_db(self, connection, sqlite_file, snapshot):
        seed_worker(
            connection['seedFolder'],
            connection['engine'],
            connection['dryrun'],
            Base.metadata)
        self.accounts = select_accounts_df(connection['engine'])
        accountString = self.accounts.to_csv()
        assert accountString == snapshot

    def test_prep_checking_df(self):
        # dbwrapper/helpers/readCsv
        input_columns = [
            'Details',
            'Description',
            'Amount',
            'Type',
            'Balance',
            'Check or Slip #',
            'Post Date',
            'Transaction Date',
            'Category'
        ]
        df = pd.DataFrame(columns=input_columns)
        result = list(prepCheckingDf(df, '0').columns)
        expected_columns = [
            'details',
            'description',
            'amount',
            'type',
            'balance',
            'checkOrSlipNumber',
            'postDate',
            'transactionDate',
            'category',
            'loadID'
        ]
        print(result)
        assert result == expected_columns
    
    def test_open_one_csv(self, connection, engine, snapshot):
        # dbwrapper/helpers/readCsv
        accounts = select_accounts_df(engine)
        resultsString = ""
        df = None
        for index, account in accounts.iterrows():
            path = f"{account['csvPath']}"
            accountPath = f"{rawCsvPath}/{path}"
            for file in os.listdir(accountPath):
                fileAndPath = f"{rawCsvPath}/{path}/{file}"
                filenameParts = file.split('.')
                filename = filenameParts[:len(filenameParts)-1][0]
                df = openOneCsv(fileAndPath)
                break
            break
        assert df.to_csv() == snapshot

    def test_get_account_history(self, connection, engine, snapshot):
        accounts = select_accounts_df(engine)
        resultsString = ""
        for index, account in accounts.iterrows():
            path = f"{account['csvPath']}"
            Session = sessionmaker(bind=engine)
            session = Session()
            allFiles = getAccountHistory(path, account['id'], session, rawCsvPath=rawCsvPath)
            print('test_get_account_history')
            resultsString = f"{resultsString}{allFiles.to_csv()}"
            print(allFiles.to_csv())

        assert resultsString==snapshot
