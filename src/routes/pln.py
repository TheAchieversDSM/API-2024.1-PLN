from typing import Union
from fastapi import APIRouter, File, UploadFile

from ..controller.hot_topics import GetHotTopicsByCategory

router = APIRouter(prefix="/pln", tags=["pln"])


@router.post("/hot_topics/{category}")
async def hot_topics(category: str, csv: UploadFile = File(), limit: Union[str, int] = "max"):
    return GetHotTopicsByCategory(category, csv, limit).process_by_categories()
