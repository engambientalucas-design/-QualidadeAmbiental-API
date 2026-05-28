from pydantic import BaseModel, ConfigDict, Field


class ParametroResponse(BaseModel):
    id_parametro: int = Field(..., examples=[1])
    nome_parametro: str = Field(..., examples=["Turbidez"])
    unidade_medida: str | None = Field(default=None, examples=["NTU"])
    categoria: str | None = Field(default=None, examples=["Fisico-quimico"])
    descricao: str | None = Field(default=None, examples=["Parametro de qualidade da agua."])
    ativo: bool = Field(..., examples=[True])

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):
    page: int = Field(..., ge=1, examples=[1])
    page_size: int = Field(..., ge=1, le=100, examples=[20])
    total: int = Field(..., ge=0, examples=[12])


class ParametroListResponse(BaseModel):
    success: bool = Field(default=True, examples=[True])
    message: str = Field(default="Consulta realizada com sucesso.")
    data: list[ParametroResponse]
    pagination: PaginationResponse
