from pydantic import BaseModel

class ProductSummaryModel(BaseModel):
    amount: int
    text: str
    product_id: int