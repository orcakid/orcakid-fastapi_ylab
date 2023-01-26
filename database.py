from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()

# локальная база
DATABASE_URL_LOCAL = f'postgresql://{os.environ.get("DB_USER_LOCAL")}:{os.environ.get("DB_PASSWORD_LOCAL")}@localhost/{os.environ.get("DB_NAME_LOCAL")}'
# бд контейнеров приложения и базы данных
DATABASE_URL = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@db:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
# бд контейнеров тест
DATABASE_URL_TESTING = f'postgresql://{os.environ.get("DB_USER_TESTING")}:{os.environ.get("DB_PASSWORD_TESTING")}@db_test:{os.environ.get("DB_PORT_TESTING")}/{os.environ.get("DB_NAME_TESTING")}'


engine = create_engine(DATABASE_URL_LOCAL, echo=True)

BASE = declarative_base()

Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_init():
    BASE.metadata.create_all(engine)


def get_db() -> Generator:
    try:
        db = Session_local()
        yield db
    finally:
        db.close()
