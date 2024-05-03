from src.config.database import db_session
from src.controller.execute_pipeline import ExecutePipeline
from typing import Union
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/pln", tags=["pln"])

@router.post("/execute", description="Rota que vai executar toda a pipeline do PLN")
async def execute_pipeline(file: UploadFile = File(description="Arquivo .csv"), limit: Union[str, int] = "max", db: AsyncSession =  Depends(db_session)):
    return await ExecutePipeline(file, db).processing()