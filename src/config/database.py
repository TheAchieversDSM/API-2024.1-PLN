# orm/session_manager.py
from typing import AsyncGenerator
from fastapi import Depends
from src.config.settings import settings
from .db.database_session import DatabaseSessionManager
from sqlalchemy.ext.asyncio import AsyncSession
from .db.database_session import db_manager

async def init_db():
    await db_manager.init(settings.DATABASE_URI)

async def finish_db():
    await db_manager.close()

def db_conn() -> DatabaseSessionManager:
    return db_manager

async def db_session(manager=Depends(db_conn)) -> AsyncGenerator[AsyncSession, None]:
    async with manager.session() as session:
        yield session