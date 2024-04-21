from sqlalchemy import BigInteger, Date, Integer, String
from src.schemas.commet import CommentModel
from ..config.db.orm import OrmBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date as pDate

class Comment(OrmBase):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    rating: Mapped[int] = mapped_column(Integer)
    date: Mapped[pDate] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String)  # Corrigido para String
    state: Mapped[str] = mapped_column(String)
    productId: Mapped[int] = mapped_column(BigInteger)  # Corrigido para Integer

    async def insert(self, data: CommentModel):
        print(data)