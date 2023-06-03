import pandas as pd
#from dbwrapper.helpers.readCsv import setDateColumns
from . import setDateColumns
#from dbwrapper.helpers.readCsv import setDateColumns

def query_to_df(query, convert_date_columns=True):
    result = query.all()
    column_names = [ x['name'] for x in query.column_descriptions]
    df = pd.DataFrame(result, columns=column_names)
    if convert_date_columns:
        df = setDateColumns(df)
    return df

