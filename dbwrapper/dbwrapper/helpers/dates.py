import pandas as pd

def setDateColumns(df):
    columns = list(df.columns)
    date_columns = [s for s in columns if 'Date' in s]
    for column in date_columns:
        df[column] = pd.to_datetime(df[column])
    return df

def getDateColumns(path):
    columns = list(pd.read_csv(path, index_col=False, nrows=2).columns)
    date_columns = [s for s in columns if 'Date' in s]
    return date_columns
