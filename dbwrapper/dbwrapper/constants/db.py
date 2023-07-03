dbfilepath = '../db/money.sqlite'
rawCsvPath = '../db/rawTransactionHistory'
connectionString = f"sqlite:///{dbfilepath}"

def getConnectionString(env='local'):
    connectionString = {
        'local': f"sqlite:///../db/money.sqlite",
        'test': 'sqlite:///tests/mock_data/mockdb.sqlite'
    }
    if env.lower() in connectionString:
        return connectionString[env.lower()]
    return connectionString['test']

def getSeedFolder(env='local'):
    seedFolder={
        'local':    '../db/seed_data/',
        'test':     './tests/mock_data/seed_data/',
        'default':  './testsmock_data/seed_data/'
    }
    if env.lower() in seedFolder:
        return seedFolder[env.lower()]
    return seedFolder['default']