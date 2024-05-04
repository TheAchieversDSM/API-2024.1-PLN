from pydantic import BaseModel


class BaseImportModel(BaseModel):
    fileName: str
    status: str