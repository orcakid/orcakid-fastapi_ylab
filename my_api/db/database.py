import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
load_dotenv()


DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'


#engine = create_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

#Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session_local_async = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
BASE = declarative_base()


async def db_init():
    with Session_local_async.begin() as conn:
        conn.run_sync(BASE.metadata.create_all(engine))


async def get_db() -> AsyncSession:
    async with Session_local_async() as session:
        yield session
        

