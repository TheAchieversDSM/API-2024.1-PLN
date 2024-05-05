from pydantic_settings import BaseSettings
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    POSTGRES_HOST: Optional[str] = "localhost"
    POSTGRES_PORT: Optional[int] = 5432
    DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"


settings = Settings()
