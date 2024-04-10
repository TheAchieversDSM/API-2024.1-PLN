from fastapi import APIRouter, File, UploadFile
from ..controller.processamento import Processamento

router = APIRouter(prefix="/pln", tags=["pln"])


@router.post("/")
async def processamento(csv: UploadFile = File()):
    return Processamento(csv).process_data()
