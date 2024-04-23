from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.exc import SQLAlchemyError
from src.schemas.base_import import BaseImportModel
from ..config.db.orm import OrmBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class BaseImportLog(OrmBase):
    __tablename__ = "base_import_log"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    fileName: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=func.now()
    )

    async def insert(self, data: BaseImportModel, db: AsyncSession):
        try:
            insert = BaseImportLog(fileName=data.fileName, status=data.status)
            db.add(insert)
            await db.commit()
            return insert.id
        except SQLAlchemyError as e:
            await db.rollback()
            print("Erro ao inserir a base:", e)

    async def update(self, id: int, msg: str, db: AsyncSession):
        try:
            logger = await db.get(BaseImportLog, id)
            logger.status = msg
            await db.commit()
        except SQLAlchemyError:
            await db.rollback()