from ..config.db.orm import OrmBase
from src.schemas.commet import CommentModel
from datetime import date as pDate
from sqlalchemy import BigInteger, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class Comment(OrmBase):
    __tablename__ = "comment"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    rating: Mapped[int] = mapped_column(Integer)
    date: Mapped[pDate] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    productId: Mapped[int] = mapped_column(BigInteger)

    async def insert(self, data: CommentModel, db: AsyncSession):
        try:
            q = select(Comment).where(Comment.id == data.id)
            result = await db.execute(q)
            existing_product = result.scalar()
            if existing_product is None:
                new_comment = Comment(
                    id=data.id,
                    title=data.title,
                    text=data.text,
                    rating=data.rating,
                    gender=data.gender,
                    state=data.state,
                    productId=data.productId,
                    date=data.date,
                )
                db.add(new_comment)
        except SQLAlchemyError as e:
            print("Erro no comentario:", e)
