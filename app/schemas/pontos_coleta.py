from pydantic import BaseModel, ConfigDict, Field


class PontoColetaResponse(BaseModel):
    id_ponto_coleta: int = Field(..., examples=[1])
    nome_ponto: str = Field(..., examples=["Rio Cuiaba - Ponto 01"])
    tipo_ponto: str = Field(..., examples=["Corpo Hidrico"])
    municipio: str = Field(..., examples=["Cuiaba"])
    estado: str = Field(..., min_length=2, max_length=2, examples=["MT"])
    latitude: float | None = Field(default=None, examples=[-15.601234])
    longitude: float | None = Field(default=None, examples=[-56.097891])
    observacao: str | None = Field(default=None, examples=["Ponto de monitoramento ambiental."])

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):
    page: int = Field(..., ge=1, examples=[1])
    page_size: int = Field(..., ge=1, le=100, examples=[20])
    total: int = Field(..., ge=0, examples=[6])


class PontoColetaListResponse(BaseModel):
    success: bool = Field(default=True, examples=[True])
    message: str = Field(default="Consulta realizada com sucesso.")
    data: list[PontoColetaResponse]
    pagination: PaginationResponse
