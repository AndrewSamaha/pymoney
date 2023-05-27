from sqlalchemy.orm import sessionmaker

def insert_query_into_table(engine, query, dest_table):
    column_names = [ x['name'] for x in query.column_descriptions]
    results = query.all()
    Session = sessionmaker(bind=engine)
    session = Session()

    for idx, result in enumerate(results):
        row_data = dict(zip( column_names, result))
        dest_table_row = dest_table(**row_data)
        session.add(dest_table_row)

    session.commit()
    session.close()
