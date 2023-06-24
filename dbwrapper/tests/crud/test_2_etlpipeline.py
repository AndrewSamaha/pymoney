import pytest
import os
from dbwrapper import testvalue
from dbwrapper.constants import getConnectionString, getSeedFolder
from dbwrapper.helpers import seed_worker, getSeedEngine
from dbwrapper.models import Base
from dbwrapper.crud.read import select_accounts_df

class TestEtlPipeline:
    @pytest.fixture
    def connection(self, tmp_path):
        ENV = 'Test'
        dryrun = False
        seedFolder = getSeedFolder(ENV)
        connectionString = f"sqlite:///{tmp_path}/mockdb.sqlite"
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
    
    def test_create_and_seed_db(self, connection, tmp_path, snapshot):
        seed_worker(
            connection['seedFolder'],
            connection['engine'],
            connection['dryrun'],
            Base.metadata)
        accountString = select_accounts_df(connection['engine']).to_csv()
        assert accountString == snapshot

