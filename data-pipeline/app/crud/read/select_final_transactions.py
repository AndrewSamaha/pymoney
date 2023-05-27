from sqlalchemy.orm import sessionmaker
from app.main import TransactionFinal

def select_final_transactions(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
            TransactionFinal.sha256,
            TransactionFinal.postDate,
            TransactionFinal.transactionDate,
            TransactionFinal.accountId,
            TransactionFinal.amount,
            TransactionFinal.description,
            TransactionFinal.memo,
            TransactionFinal.details,
            TransactionFinal.type,
            TransactionFinal.category,
            TransactionFinal.balance,
            TransactionFinal.checkOrSlipNumber
        ).order_by(
            TransactionFinal.postDate
        )

    return query
