import pandas as pd
import os
import re
from datetime import datetime
from sqlalchemy import text

from ..constants import rawCsvPath
from ..models import Load
from . import setDateColumns, getDateColumns, hash, hashType

def openOneCsv(path):
    date_columns = getDateColumns(path)
    df = pd.read_csv(path, index_col=False, parse_dates=date_columns)
    if "Balance" in df.columns:
        df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    df[hashType] = df.apply(hash, axis=1)
    df['stagingLevel'] = 'allTransactions'
    
    return df

def prepCheckingDf(df, loadID):
    df = df.rename(columns={
        'Details': 'details',
        'Description': 'description',
        'Amount': 'amount',
        'Type': 'type',
        'Balance': 'balance',
        'Check or Slip #': 'checkOrSlipNumber',
        'Post Date': 'postDate',
        'Transaction Date': 'transactionDate',
        'Category': 'category'
    })
    df = df.drop(['seenTime'], errors='ignore')
    df['loadID'] = loadID
    return df

def getAccountHistory(path, accountId, session, rawCsvPath=rawCsvPath):
    df = None
    accountPath = f"{rawCsvPath}/{path}"
    for file in os.listdir(accountPath):
        fileAndPath = f"{rawCsvPath}/{path}/{file}"
        filenameParts = file.split('.')
        filename = filenameParts[:len(filenameParts)-1][0]

        newDf = openOneCsv(fileAndPath)

        if 'Posting Date' in newDf.columns:
            newDf['Post Date'] = newDf['Posting Date']
            newDf = newDf.drop(axis=1, columns=['Posting Date'])
        
        if session is not None:
            matchingLoads = pd.read_sql(sql=text(f"select * from loads WHERE fullFilePath = '{fileAndPath}'"), con=session.connection()) 

            if matchingLoads.shape[0] > 0:
                print(f"  skipping {matchingLoads.shape[0]}")
                continue
            
            load = Load(accountId=accountId, fullFilePath=fileAndPath)
            session.add(load)
            session.commit()
            newDf['accountId'] = accountId
            preppedDf = prepCheckingDf(newDf, load.id)

        if df is None:
            df = preppedDf
        else:
            df = pd.concat([df, preppedDf])

    if df is None:
        return None

    # Convert Date Strings to Date
    dateColumns = ['Post Date','Transaction Date']
    for dateColumn in dateColumns:
        if dateColumn in df.columns:
            df[dateColumn] = pd.to_datetime(df[dateColumn], format='%Y-%m-%d') # %m-%d-%Y

    # sort by Post Date and then sha
    df = df.sort_values(by=['postDate', 'sha256'], ascending=False)
    
    return df
