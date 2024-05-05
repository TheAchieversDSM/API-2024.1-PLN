from pydantic import BaseModel

class CategorySummaryModel(BaseModel):
    category: str
    amount: int
    text: str
    type: str