from src.schemas.base_import import BaseImportModel
from ..config.db.orm import OrmBase
from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession


class BaseImportLog(OrmBase):
    __tablename__ = "base_import_log"
    id: Mapped[int] = mapped_column( BigInteger, primary_key=True)
    fileName: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    createdAt: Mapped[datetime] = mapped_column(DateTime, index=True, default=func.now())

    async def insert(self, data: BaseImportModel, db: AsyncSession):
        try:
            insert = BaseImportLog(fileName=data.fileName, status=data.status)
            db.add(insert)
            await db.commit()
            return insert.id
        except SQLAlchemyError as e:
            print("Erro ao inserir a base:", e)
            raise

    async def update(self, id: int, status: str, db: AsyncSession):
        try:
            logger = await db.get(BaseImportLog, id)
            logger.status = status
        except SQLAlchemyError:
            raise
