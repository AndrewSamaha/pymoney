from sqlalchemy.orm import sessionmaker
from ...models import Transaction

def select_unique_staged_transactions(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
            Transaction.sha256,
            Transaction.postDate,
            Transaction.transactionDate,
            Transaction.accountId,
            Transaction.amount,
            Transaction.description,
            Transaction.memo,
            Transaction.details,
            Transaction.type,
            Transaction.category,
            Transaction.balance,
            Transaction.checkOrSlipNumber
        ).group_by(
            Transaction.sha256,
            Transaction.postDate,
            Transaction.transactionDate,
            Transaction.accountId,
            Transaction.amount,
            Transaction.description,
            Transaction.memo,
            Transaction.details,
            Transaction.type,
            Transaction.category,
            Transaction.balance,
            Transaction.checkOrSlipNumber,
        ).order_by(
            Transaction.postDate
        )

    session.close()
    
    return query
