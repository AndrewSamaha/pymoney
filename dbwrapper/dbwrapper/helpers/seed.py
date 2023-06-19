import os
from sqlalchemy import text

def seed_worker(seedFolder=None, engine=None, dryrun=False, metadata=None):
    print(f"running seed_worker(dryrun={dryrun})")
    if not seedFolder:
        raise ValueError('No seedFolder specified, expecting something like db/seed_data')
    
    if not engine:
        raise ValueError('No engine specified.')

    if not metadata:
        raise ValueError('No metadata supplied.')

    metadata.create_all(bind=engine, checkfirst=True)

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