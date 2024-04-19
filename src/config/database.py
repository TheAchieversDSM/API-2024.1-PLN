from fastapi import Depends
from asyncio import current_task
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, AsyncAttrs
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .settings import settings
from typing import AsyncGenerator

class Base(AsyncAttrs, DeclarativeBase):
    pass

_db_conn: AsyncSession = None

async def create_session():
    global _db_conn
    _db_conn = create_async_engine(
        str(settings.DATABASE_URI),
        **settings.SQLALCHEMY_ENGINE_OPTIONS,
    )
    
    async with _db_conn.begin() as conn:
        await conn.execute(text(f"SET search_path TO {settings.POSTGRES_SCHEMA}"))
        await conn.run_sync(Base.metadata.create_all)

async def finish_session():
    global _db_conn
    if _db_conn:
        await _db_conn.close()

async def get_db() -> AsyncSession:
    assert _db_conn is not None
    return _db_conn

async def db_session(engine = Depends(create_session)) -> AsyncGenerator:
    async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async_session = async_scoped_session(async_session_factory, scopefunc=current_task)
    async with async_session() as session:
        yield session