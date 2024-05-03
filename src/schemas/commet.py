from pydantic import BaseModel
from datetime import date


class CommentModel(BaseModel):
    id: str
    title: str
    text: str
    rating: int
    date: date
    gender: str
    state: str
    productId: int

    class Config:
        arbitrary_types_allowed = True
