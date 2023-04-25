import pandas as pd
import os
import re
from datetime import datetime

from app.helpers.hash import hash, hashType
from app.constants.db import rawCsvPath

def openOneCsv(path):
    df = pd.read_csv(path, index_col=False)
    df[hashType] = df.apply(hash, axis=1)
    df['seenTime'] = datetime.now()
    df['filename'] = path
    return df

def getAccountHistory(path):
    df = None
    accountPath = f"{rawCsvPath}/{path}"
    for file in os.listdir(accountPath):
        fileAndPath = f"{rawCsvPath}/{path}/{file}"
        filenameParts = file.split('.')
        extension = filenameParts[-1]
        filename = filenameParts[:len(filenameParts)-1][0]
        print(f"reading {filename}")

        pattern = r'(\d{4}|\d{8})'
        pattern = r'(\d{8})'
        dates = re.findall(pattern, filename)
            
        if df is None:
            df = openOneCsv(fileAndPath)
        else:
            df = pd.concat([df, openOneCsv(fileAndPath)])

        #checkingdf = pd.read_csv(path, index_col=False)
    if 'Posting Date' in df.columns:
        df['Post Date'] = df['Posting Date']
        df = df.drop(axis=1, columns=['Posting Date'])
        # cols = df.columns
        # cols = cols[-1:] + cols[:-1]
        # df = df[cols]
    
    # Convert Date Strings to Date
    dateColumns = ['Post Date','Transaction Date']
    for dateColumn in dateColumns:
        if dateColumn in df.columns:
            df[dateColumn] = pd.to_datetime(df[dateColumn], format='%m/%d/%Y')

    # sort by Post Date and then sha
    df = df.sort_values(by=['Post Date', 'sha256'], ascending=False)
    
    return df