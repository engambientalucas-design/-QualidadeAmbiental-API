from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "QualidadeAmbiental API"
    PROJECT_DESCRIPTION: str = (
        "API REST para consulta de dados de qualidade ambiental a partir do "
        "banco SQL Server QualidadeAmbiental."
    )
    API_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    ENVIRONMENT: str = "local"
    DEBUG: bool = True

    DB_SERVER: str = Field(default="localhost", description="Servidor SQL Server")
    DB_PORT: Optional[int] = Field(default=1433, description="Porta do SQL Server")
    DB_NAME: str = Field(default="QualidadeAmbiental", description="Nome do banco")
    DB_USER: str = Field(default="", description="Usuário do banco")
    DB_PASSWORD: str = Field(default="", description="Senha do banco")
    DB_DRIVER: str = Field(default="ODBC Driver 18 for SQL Server")
    DB_ENCRYPT: str = Field(default="no")
    DB_TRUST_SERVER_CERTIFICATE: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="QA_API_",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("DB_PORT", mode="before")
    @classmethod
    def empty_db_port_as_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
