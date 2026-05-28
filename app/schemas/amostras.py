from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class AmostraResponse(BaseModel):
    id_amostra: int = Field(..., examples=[1])
    codigo_amostra: str = Field(..., examples=["AM-2026-001"])
    data_coleta: date = Field(..., examples=["2026-04-01"])
    hora_coleta: time | None = Field(default=None, examples=["08:30:00"])
    id_ponto_coleta: int = Field(..., examples=[1])
    nome_ponto: str = Field(..., examples=["Captacao Rio Norte"])
    municipio: str = Field(..., examples=["Cuiaba"])
    estado: str = Field(..., min_length=2, max_length=2, examples=["MT"])
    id_tipo_amostra: int = Field(..., examples=[1])
    nome_tipo_amostra: str = Field(..., examples=["Agua Bruta"])
    id_status: int = Field(..., examples=[1])
    nome_status: str = Field(..., examples=["Coletada"])
    id_responsavel: int = Field(..., examples=[1])
    nome_responsavel: str = Field(..., examples=["Maria Silva"])
    observacao: str | None = Field(default=None, examples=["Coleta realizada sem intercorrencias."])

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):
    page: int = Field(..., ge=1, examples=[1])
    page_size: int = Field(..., ge=1, le=100, examples=[20])
    total: int = Field(..., ge=0, examples=[6])


class AmostraListResponse(BaseModel):
    success: bool = Field(default=True, examples=[True])
    message: str = Field(default="Consulta realizada com sucesso.")
    data: list[AmostraResponse]
    pagination: PaginationResponse
