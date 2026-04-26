# async_url="postgresql+asyncpg://postgres@localhost:5432/assignment5"
# sync_url="postgresql://postgres@localhost:5432/assignment5"

async_url="sqlite+aiosqlite:///./test.db"
sync_url="sqlite:///./test.db"

from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine

sync_engine=create_engine(url=sync_url,echo=True)
async_engine=create_async_engine(url=async_url,echo=True)

sync_session=sessionmaker(class_=Session,bind=sync_engine,expire_on_commit=False)
async_session=async_sessionmaker(class_=AsyncSession,bind=async_engine,expire_on_commit=False)