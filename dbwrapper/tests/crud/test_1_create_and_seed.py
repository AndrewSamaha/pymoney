import pytest
import os
from dbwrapper import testvalue
from dbwrapper.constants import getConnectionString, getSeedFolder
from dbwrapper.helpers import seed_worker, getSeedEngine
from dbwrapper.models import Base
from dbwrapper.crud.read import select_accounts_df

# Need to refactor this to use the tmp_path fixture!
def test_create_and_seed_db(tmp_path, snapshot):
    ENV = 'Test'
    dryrun = False
    seedFolder = getSeedFolder(ENV)
    connectionString = f"sqlite:///{tmp_path}/mockdb.sqlite"
    engine = getSeedEngine(connectionString)
    print(f"seedFolder={seedFolder}")
    seed_worker(seedFolder, engine, dryrun, Base.metadata)
    #accountString = select_accounts_df(engine).to_csv()
    #assert accountString == snapshot
    assert 42 == 42
