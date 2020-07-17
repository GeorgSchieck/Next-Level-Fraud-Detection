# coding: utf-8
from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, SmallInteger, String, func, or_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine

Base = automap_base()
metadata = Base.metadata
connection_string = 'postgresql://postgres:Exploration@h2655330.stratoserver.net:1312/'

# Einführung der Create-Funktionen, um die Datenbank zentral über einen
# Entrypoint nutzen zu können
def CreateSession():
    engine = create_engine(connection_string)
    Base.prepare(engine, reflect=True)
    return Session(engine)

class Transaction(Base):
    __tablename__ = 'Transaction'

    tx_id = Column(BigInteger, primary_key=True)
    step = Column(SmallInteger, nullable=False)
    type = Column(String(50), nullable=False)
    amount = Column(Numeric, nullable=False)
    nameOrig = Column(String(50), nullable=False)
    oldbalanceOrg = Column(Numeric, nullable=False)
    newbalanceOrig = Column(Numeric, nullable=False)
    nameDest = Column(String(50), nullable=False)
    oldbalanceDest = Column(Numeric, nullable=False)
    newbalanceDest = Column(Numeric, nullable=False)


class TransactionRating(Transaction):
    __tablename__ = 'Transaction_Rating'

    tx_id = Column(ForeignKey('Transaction.tx_id'), primary_key=True, index=True)
    isFraud = Column(SmallInteger)
    isFlaggedFraud = Column(SmallInteger)


class TransactionPreprocessed(Base):
    __tablename__ = 'Transaction_preprocessed'

    tx_id = Column(BigInteger, primary_key=True)
    amount = Column(Numeric, nullable=False)
    oldbalanceOrg = Column(Numeric, nullable=False)
    newbalanceOrig = Column(Numeric, nullable=False)
    PctChangeOrig = Column(Numeric, nullable=False)
    HourOfTheDay = Column(SmallInteger, nullable=False)
    RelativePctTxToDest = Column(Numeric, nullable=False)
    CASH_IN = Column(SmallInteger, nullable=False)
    CASH_OUT = Column(SmallInteger, nullable=False)
    DEBIT = Column(SmallInteger, nullable=False)
    PAYMENT = Column(SmallInteger, nullable=False)
    TRANSFER = Column(SmallInteger, nullable=False)