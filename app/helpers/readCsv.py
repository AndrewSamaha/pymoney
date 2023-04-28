import pandas as pd
import os
import re
from datetime import datetime

from app.helpers.hash import hash, hashType
from app.constants.db import rawCsvPath
from app.models.Load import Load

def openOneCsv(path):
    df = pd.read_csv(path, index_col=False)
    df[hashType] = df.apply(hash, axis=1)
    df['seenTime'] = datetime.now()
    df['filename'] = path
    return df

def getAccountHistory(path, accountId, session):
    df = None
    accountPath = f"{rawCsvPath}/{path}"
    for file in os.listdir(accountPath):
        fileAndPath = f"{rawCsvPath}/{path}/{file}"
        filenameParts = file.split('.')
        extension = filenameParts[-1]
        filename = filenameParts[:len(filenameParts)-1][0]
        print(f"reading {filename}")

        newDf = openOneCsv(fileAndPath)

        if 'Posting Date' in newDf.columns:
            newDf['Post Date'] = newDf['Posting Date']
            newDf = newDf.drop(axis=1, columns=['Posting Date'])
        
        if session is not None:
            load = Load(accountId=accountId, fullFilePath=fileAndPath)
            session.add(load)
            session.commit()

        if df is None:
            df = newDf
        else:
            df = pd.concat([df, newDf])


    # Convert Date Strings to Date
    dateColumns = ['Post Date','Transaction Date']
    for dateColumn in dateColumns:
        if dateColumn in df.columns:
            df[dateColumn] = pd.to_datetime(df[dateColumn], format='%m/%d/%Y')

    # sort by Post Date and then sha
    df = df.sort_values(by=['Post Date', 'sha256'], ascending=False)
    
    return df