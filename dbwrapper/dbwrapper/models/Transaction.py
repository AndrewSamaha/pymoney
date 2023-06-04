from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, declarative_mixin, declared_attr
from .Base import Base

@declarative_mixin
class Transaction(Base):
    __tablename__ = 'transactions_all'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    accountId = Column(Integer)

    # checking account fields 8115
    details = Column(String)
    
    type = Column(String)
    balance = Column(Float)
    checkOrSlipNumber = Column(String)

    # credit account fields
    transactionDate = Column(String)
    category = Column(String)
    memo = Column(String)

    # shared fields
    postDate = Column(String)
    description = Column(String)
    amount = Column(Float)

    # added fields
    sha256 = Column(String)
    loadID = mapped_column(ForeignKey('loads.id'))

    # necessary to organize
    stagingLevel = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'allTransactions',
        'polymorphic_on': stagingLevel
    }

class TransactionFinal(Transaction):
    __tablename__ = 'transactions_final'
    id = Column(Integer, ForeignKey('transactions_all.id'), primary_key=True, autoincrement=True)
    __mapper_args__ = {'polymorphic_identity': 'final_transaction'}
    
    # # Columns from parent class that should have been included anyway
    # name = Column(String)
    # accountId = Column(Integer)

    # # checking account fields 8115
    # details = Column(String)
    
    # type = Column(String)
    # balance = Column(Float)
    # checkOrSlipNumber = Column(String)

    # # credit account fields
    # transactionDate = Column(String)
    # category = Column(String)
    # memo = Column(String)

    # # shared fields
    # postDate = Column(String)
    # description = Column(String)
    # amount = Column(Float)

    # # added fields
    # sha256 = Column(String)
    # loadID = mapped_column(ForeignKey('loads.id'))

    # # necessary to organize
    # stagingLevel = Column(String)


# Transaction.children = relationship(
#     TransactionFinal,
#     cascade='all, delete-orphan',
#     single_parent=True,
#     innerjoin=True,
#     viewonly=True,
#     order_by='TransactionFinal.id'
# )

#TransactionFinal.metadata.create_all(bind=engine, checkfirst=True)

# class TransactionAllLoads(Base, Transaction):
#     __tablename__ = 'transactions_all_loads'
#     id = Column(Integer, primary_key=True)

# TransactionAllLoads.metadata.create_all(bind=engine, checkfirst=True)
