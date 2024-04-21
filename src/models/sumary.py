from sqlalchemy import BigInteger, ForeignKey, Integer, String
from ..config.db.orm import OrmBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProductSummary(OrmBase):
    __tablename__ = "product_summary"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    productId: Mapped[int] = mapped_column(BigInteger, ForeignKey("product.id"))
    product: Mapped["Product"] = relationship("Product", back_populates="summary")  # type: ignore  # noqa: F821
