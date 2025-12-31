from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from decouple import config
from typing import Annotated,AsyncGenerator
from fastapi import Depends
# DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/db_name

DB_USER=config("DB_USER")
DB_PORT=config("DB_PORT",cast=int)
DB_NAME=config("DB_NAME")
DB_HOST = config("DB_HOST")
DB_PASS=config("DB_PASS")

DATABASE_URL=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(bind=engine,expire_on_commit=False, class_=__annotations__)

async def get_session()-> AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session


sessionDep = Annotated[AsyncSession, Depends(get_session)]