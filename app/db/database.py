from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB1_URL = 'sqlite:///authors_database.db'
DB2_URL = 'sqlite:///logs_database.db'

engine_db1 = create_engine(DB1_URL, echo=True)
engine_db2 = create_engine(DB2_URL, echo=True)

session_local_db1 = sessionmaker(autocommit=False, autoflush=False, bind=engine_db1)
session_local_db2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_db2)


def get_db1():
    with session_local_db1() as db:
        yield db


def get_db2():
    with session_local_db2() as db:
        yield db
