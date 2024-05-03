from pydantic import BaseModel
from datetime import date


class CommentModel(BaseModel):
    id: str
    title: str
    text: str
    rating: int
    age: int
    date: date
    gender: str
    state: str
    productId: int
    recommended: bool

    class Config:
        arbitrary_types_allowed = True
