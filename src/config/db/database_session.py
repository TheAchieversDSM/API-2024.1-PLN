import contextlib
from typing import AsyncGenerator, Optional
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

from src.config.settings import settings


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    async def init(self, db_url: str) -> None:
        self._engine = create_async_engine(
            url=str(db_url),
            **(settings.SQLALCHEMY_ENGINE_OPTIONS),
        )
        sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self._sessionmaker = async_scoped_session(sessionmaker, scopefunc=current_task)

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()
