import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


DATABASE_URL = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'


engine = create_engine(DATABASE_URL)
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BASE = declarative_base()


def db_init():
    BASE.metadata.create_all(engine)


def get_db() -> Generator:
    try:
        db = Session_local()
        yield db
    finally:
        db.close()
