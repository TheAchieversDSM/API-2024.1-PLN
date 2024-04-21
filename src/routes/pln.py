from typing import Union
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import db_session
from src.controller.execute_pipeline import ExecutePipeline
from src.controller.most_comments import GetMostCommentsList

from ..controller.hot_topics import GetHotTopicsByCategory

router = APIRouter(prefix="/pln", tags=["pln"])


@router.post("/hotTopics/{category}", description="Rota que trás os topicos mais frequente da categoria fornecida")
async def hot_topics(category: str, csv: UploadFile = File(description="Arquivo .csv"), limit: Union[str, int] = "max"):
    return GetHotTopicsByCategory(category, csv, limit).process_by_categories()

@router.post("/mostComments/{category}", description="Rota para retornar os que é mais comentados com base na categoria fornecida")
async def most_comments(category: str, file: UploadFile = File(description="Arquivo .csv"), limit: Union[str, int] = "max"):
    return GetMostCommentsList(category, file, limit).process_by_categories()

@router.post("/execute", description="Rota que vai executar toda a pipeline do PLN")
async def execute_pipeline(file: UploadFile = File(description="Arquivo .csv"), limit: Union[str, int] = "max", db: AsyncSession =  Depends(db_session)):
    return await ExecutePipeline(file, db).processing()