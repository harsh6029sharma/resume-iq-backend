from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession,AsyncAttrs
from dotenv import load_dotenv
from typing import Annotated,AsyncGenerator
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
import os
# DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/db_name

load_dotenv()

# DB_USER=os.getenv("DB_USER")
# DB_PORT=os.getenv("DB_PORT")
# DB_NAME=os.getenv("DB_NAME")
# DB_HOST=os.getenv("DB_HOST")
# DB_PASS=os.getenv("DB_PASS")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path= os.path.join(BASE_DIR, "sqlite.db")

DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False},echo=True, future=True)

async_session = async_sessionmaker(bind=engine,expire_on_commit=False, class_= AsyncSession)

class Base(AsyncAttrs,DeclarativeBase):
    pass

async def create_tables():
    from app.models.models import User, RefreshToken,Job,Analysis,Candidate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables Created...")

async def get_session()-> AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        yield session


sessionDep = Annotated[AsyncSession, Depends(get_session)]