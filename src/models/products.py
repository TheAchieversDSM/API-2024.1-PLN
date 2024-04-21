from sqlalchemy import BigInteger, String
from sqlalchemy.exc import SQLAlchemyError
from ..config.db.orm import OrmBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.sumary import ProductSummary
from src.schemas.product import ProductModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

class Product(OrmBase):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True,)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    subcategory: Mapped[str] = mapped_column(String)
    externalId: Mapped[str] = mapped_column(String, nullable=True) 

    summary: Mapped['ProductSummary'] = relationship("ProductSummary", back_populates="product")

    async def insert(self, data: ProductModel, db: AsyncSession):
        try:
            q = select(Product).where(Product.id == data.id)
            result = await db.execute(q)
            existing_product = result.scalar()

            if existing_product is None:
                new_product = Product(
                    id=data.id,
                    name=data.name,
                    category=data.category,
                    subcategory=data.subcategory,
                    externalId=data.externalId
                )
                db.add(new_product)
                await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            print("Produto já existe na base de dados:", e)