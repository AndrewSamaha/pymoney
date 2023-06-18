from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import path
import sys
import os
import toml
import argparse
from dotenv import load_dotenv

# directory reach/ this lets us load modules from ../app
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)


from  dbwrapper.constants import connectionString as defaultConnectionString
load_dotenv()


def getSeedFolder(env):
    seedFolder={
        'local':    '../db/seed_data/',
        'test':     './tests/mock_data/seed_data/',
        'default':  './testsmock_data/seed_data/'
    }
    if env.lower() in seedFolder:
        return seedFolder[env.lower()]
    return seedFolder['default']

def getSeedEngine(connectionString=defaultConnectionString, engine=None):
    if engine:
        return engine
    return create_engine(connectionString, echo=True)

# This will be typically be called by seed
def seed_worker(seedFolder=None, connectionString=defaultConnectionString, engine=None, dryrun=False):
    print(f"running seed_worker(dryrun={dryrun})")
    if not seedFolder:
        raise ValueError('No seedFolder specified, expecting something like db/seed_data')
    
    if not connectionString:
        raise ValueError('No connectionString specified.')
    #quit()
    engine = getSeedEngine(connectionString, engine)

    for filename in os.listdir(seedFolder):
        filepath = f"{seedFolder}/{filename}"
        print(filepath)
        file = open(filepath, 'r')
        lines = file.readlines()
        conn = engine.connect()

        for seedline in lines:
            print(seedline)
            conn.execute(text(seedline))
            if not dryrun: conn.commit()

        if dryrun:
            print("dryrun=True. Rolling back seed.")
            conn.rollback()
        
        conn.close()

# This is a wrapper for seed_worker
def seed(connectionString=defaultConnectionString, engine=None, dryrunCLI=None):
    seedFolder = getSeedFolder(os.environ.get("ENVIRONMENT"))
    print(f"environment={os.environ.get('ENVIRONMENT')}")
    print(f"seedFolder={seedFolder}")
    print(f"connectionString={connectionString}")
    print(f"SEED_DRYRUN={os.environ.get('SEED_DRYRUN')}")
    dryrunENV = os.environ.get("SEED_DRYRUN").lower() in ['true', '1', 'yes', 'on'] if os.environ.get("SEED_DRYRUN") is not None else False
    
    if dryrunCLI or dryrunENV: dryrun = True
    else: dryrun = False

    seed_worker(seedFolder, connectionString, engine, dryrun)


def verifyPath():
    projectName = 'dbwrapper'
    projectToml = './pyproject.toml'
    exceptionMessage = 'This seed script is intended to be run from the dbwrapper root (e.g., the folder also containing a scripts/ folder and dbwrappers readme.md).'
    if os.getcwd().split(os.sep)[-1] != projectName: raise Exception(f"{exceptionMessage}.  It should not be run from {os.getcwd()}.")
    if not os.path.exists(projectToml): raise Exception(f"{exceptionMessage}. {projectToml} was not found!")
    data = toml.load(projectToml)
    if not data['tool']['poetry']['name'] == projectName: raise Exception(f"{exceptionMessage}. {projectToml} was but did not contain the correct value for tool.poetry.name!")
    

if __name__ == "__main__":
    verifyPath()
    parser = argparse.ArgumentParser()
    parser.add_argument('--dryrun', action='store_true', help='Use this option to perform a dry run of the seed script WITHOUT committing to the database.')
    parser.add_argument('--apply', action='store_true', help='Use this option to apply the seed.')
    args = parser.parse_args()
    apply = args.apply
    dryrun = args.dryrun
    if (apply and dryrun) or (not apply and not dryrun):
        parser.print_help()
        print('Note: At least one argument MUST be provided.')
        quit()
    seed(connectionString=defaultConnectionString, engine=None, dryrunCLI=dryrun)
