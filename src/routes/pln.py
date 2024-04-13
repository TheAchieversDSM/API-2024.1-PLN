from typing import Union
from fastapi import APIRouter, File, UploadFile

from src.controller.most_comments import GetMostCommentsList

from ..controller.hot_topics import GetHotTopicsByCategory

router = APIRouter(prefix="/pln", tags=["pln"])


@router.post("/hotTopics/{category}")
async def hot_topics(category: str, csv: UploadFile = File(), limit: Union[str, int] = "max"):
    return GetHotTopicsByCategory(category, csv, limit).process_by_categories()

@router.post("/mostComments/{category}")
async def most_comments(category: str, csv: UploadFile = File(), limit: Union[str, int] = "max"):
    return GetMostCommentsList(category, csv, limit).process_by_categories()