from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL,**DATABASE_PARAMS)

async_session_maker =  async_sessionmaker(bind=engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass



# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
#
# DB_HOST = 'localhost'
# DB_PORT = 5432
# DB_USER = '1234'
# DB_PASS = '1234'
# DB_NAME = '1234'
#
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
#
# engine = create_async_engine(DATABASE_URL)
#
# async_session_maker = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)
#
# class Base(DeclarativeBase):
#     pass
