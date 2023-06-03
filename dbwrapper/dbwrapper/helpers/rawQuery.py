def rawQuery(sql, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(text(sql))

    # Process the result
    for idx, row in enumerate(result):
        print(row)
        #if idx > 5: break

    # Close the result set and the connection
    session.close()