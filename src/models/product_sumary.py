from src.schemas.product_summary import ProductSummaryModel
from ..config.db.orm import OrmBase
from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ProductSummary(OrmBase):
    __tablename__ = "product_summary"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    sentiment_review: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product.id"))
    product: Mapped["Product"] = relationship("Product", back_populates="summary")  # type: ignore  # noqa: F821

    async def insert(self, data: ProductSummaryModel, db: AsyncSession):
        try:
            q = (
                select(ProductSummary)
                .where(ProductSummary.product_id == data.product_id)
                .where(ProductSummary.text == data.text)
            )
            result = await db.execute(q)
            existing_product = result.scalar()
            if existing_product:
                existing_product.amount = data.amount
                return
            insert = ProductSummary(
                amount=data.amount,
                text=data.text,
                product_id=data.product_id,
                sentiment_review=data.sentiment_review
            )
            db.add(insert)
        except SQLAlchemyError as e:
            print("[ProductSummary - insert]", e)