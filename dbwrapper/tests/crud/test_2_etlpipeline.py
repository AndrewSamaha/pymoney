import pytest
import os
from sqlalchemy.orm import sessionmaker
from dbwrapper import testvalue
from dbwrapper.constants import getConnectionString, getSeedFolder
from dbwrapper.helpers import seed_worker, getSeedEngine, getAccountHistory
from dbwrapper.models import Base
from dbwrapper.crud.read import select_accounts_df

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

    def test_get_account_history(self, connection, engine, snapshot):
        print("inside test_get_account_history")
        accounts = select_accounts_df(engine)
        resultsString = ""
        for index, account in accounts.iterrows():
            path = f"{account['csvPath']}"
            Session = sessionmaker(bind=engine)
            session = Session()
            #print(f"os.getcwd()={os.getcwd()}")
            #print(f"path={path}")
            allFiles = getAccountHistory(path, account['id'], session, rawCsvPath='tests/mock_data/rawTransactionHistory')
            print('test_get_account_history')
            resultsString = f"{resultsString}{allFiles.to_csv()}"
            print(allFiles.to_csv())

        assert resultsString==snapshot
