from typing import List, Union
from fastapi import APIRouter

from src.controller.hot_topics import GetHotTopicsByCategory
from src.controller.most_comments import GetMostCommentsList
from src.schemas.request import Review


router = APIRouter(prefix="/pln", tags=["pln"])


@router.post("/hotTopics/{category}")
async def hot_topics(category: str, data: List[Review], limit: Union[str, int] = "max"):
    return GetHotTopicsByCategory(category, data, limit).process_by_categories()

@router.post("/mostComments/{category}")
async def most_comments(category: str, data: List[Review], limit: Union[str, int] = "max"):
    return GetMostCommentsList(category, data, limit).process_by_categories()