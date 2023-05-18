import pandas as pd
import os
import re
from datetime import datetime
from sqlalchemy import text

from app.helpers.hash import hash, hashType
from app.constants.db import rawCsvPath
from app.models.Load import Load

def setDateColumns(df):
    columns = list(df.columns)
    date_columns = [s for s in columns if 'Date' in s]
    for column in date_columns:
        print(f"  converting [{column}] to datetime")
        df[column] = pd.to_datetime(df[column])
    return df

def getDateColumns(path):
    columns = list(pd.read_csv(path, index_col=False, nrows=2).columns)
    date_columns = [s for s in columns if 'Date' in s]
    return date_columns

def openOneCsv(path):
    date_columns = getDateColumns(path)
    print(f"reading {path} with these date columns: {date_columns}")
    df = pd.read_csv(path, index_col=False, parse_dates=date_columns)
    if "Balance" in df.columns:
        print(" setting Balance to numeric")
        df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    print(f"column types: {df.dtypes}")
    print(f". all columns={df.columns}")
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

def getAccountHistory(path, accountId, session):
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