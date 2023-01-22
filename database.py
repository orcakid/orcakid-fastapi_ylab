from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator


DATABASE_URL = 'postgresql://postgres:orca123@localhost/y_lab'
engine = create_engine(DATABASE_URL, echo=True)

BASE = declarative_base()
Session_local = sessionmaker(bind=engine)


def get_db() -> Generator:
    try:
        db = Session_local()
        yield db
    finally:
        db.close()
