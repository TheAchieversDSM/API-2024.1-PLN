from src.schemas import CategorySummaryModel
from ..config.db.orm import OrmBase
from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CategorySummary(OrmBase):
    __tablename__ = "category_summary"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)

    async def insert(self, data: CategorySummaryModel, db: AsyncSession):
        try:
            q = (
                select(CategorySummary)
                .where(CategorySummary.category == data.category)
                .where(CategorySummary.text == data.text)
            )
            result = await db.execute(q)
            existing_category = result.scalar()
            if existing_category:
                existing_category.amount = data.amount
                return
            new_summary = CategorySummary(
                amount=data.amount,
                text=data.text,
                type=data.type,
                category=data.category,
            )
            db.add(new_summary)
        except SQLAlchemyError as e:
            print(f"[CategorySummary - insert] Error while inserting summary: {data}")
            print("[ERROR] ", e)
