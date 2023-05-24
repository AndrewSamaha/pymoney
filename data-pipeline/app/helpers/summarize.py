def summarize(search, pdf):
    sdf = pdf[pdf['description'].str.contains(search, case=False)]
    display(sdf)
    amountSum = sdf['amount'].sum()
    numTransactions = sdf.shape[0]
    if numTransactions <= 0: return
    print(f"total number of transactions= {numTransactions}")
    print(f"sum= {amountSum}")
    print(f"avg cost per transaction= {round(amountSum/numTransactions, 2)}")
    latestDate = sdf.iloc[0]['postDate']
    startingDate = sdf.iloc[-1]['postDate']
    totalDays = (latestDate - startingDate).days
    print(f"dates= {startingDate} to {latestDate}, total days={totalDays}")
    avgDaysBetweenTransaction = totalDays / numTransactions
    print(f"avg days between transaction= {avgDaysBetweenTransaction}")
    amountSum
    costPerMonth = amountSum / (totalDays / 30.437)
    print(f"avg cost per month= {costPerMonth}")
