from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()

#DATABASE_URL = 'postgresql://postgres:orca123@localhost/y_lab'
DATABASE_URL = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@localhost/{os.environ.get("DB_NAME")}'
DATABASE_URL_TEST = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL, echo=True)
engine_test = create_engine(
    DATABASE_URL_TEST, connect_args={"check_same_thread": False}
)

BASE = declarative_base()
#Session_local = sessionmaker(bind=engine)
Session_local = sessionmaker(bind=engine_test)


def get_db() -> Generator:
    try:
        db = Session_local()
        yield db
    finally:
        db.close()