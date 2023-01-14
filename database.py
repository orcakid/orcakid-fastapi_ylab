from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'postgresql://postgres:orca123@localhost/y_lab'
engine = create_engine(DATABASE_URL, echo=True)

BASE = declarative_base()
Session_local = sessionmaker(bind=engine)
