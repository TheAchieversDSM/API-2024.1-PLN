from typing import Optional
from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    name: str
    category: str
    subcategory: str
    externalId: Optional[str]