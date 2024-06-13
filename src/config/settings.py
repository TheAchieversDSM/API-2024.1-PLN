from pydantic_settings import BaseSettings
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, field_validator, ConfigDict


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
    # Pkl
    PKL_MODELO_TREINO: str = "modelo_treinado.pkl"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        
    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_HOST"],
            port=info.data["POSTGRES_PORT"],
            path=f"{info.data['POSTGRES_DB'] or ''}",
        )

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")


settings = Settings()
