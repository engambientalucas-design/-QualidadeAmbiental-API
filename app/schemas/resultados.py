from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class ResultadoResponse(BaseModel):
    id_resultado: int = Field(..., examples=[72])
    id_amostra: int = Field(..., examples=[6])
    codigo_amostra: str = Field(..., examples=["QA-2026-006"])
    data_coleta: date = Field(..., examples=["2026-04-03"])
    hora_coleta: time | None = Field(default=None, examples=["11:15:00"])
    id_tipo_amostra: int = Field(..., examples=[2])
    nome_tipo_amostra: str = Field(..., examples=["Agua Tratada"])
    id_ponto_coleta: int = Field(..., examples=[6])
    nome_ponto: str = Field(..., examples=["Reservatorio Bairro Leste"])
    tipo_ponto: str = Field(..., examples=["Reservatorio"])
    municipio: str = Field(..., examples=["Cuiaba"])
    estado: str = Field(..., min_length=2, max_length=2, examples=["MT"])
    id_responsavel: int = Field(..., examples=[4])
    nome_responsavel: str = Field(..., examples=["Joao Pereira"])
    id_status: int = Field(..., examples=[3])
    nome_status: str = Field(..., examples=["Concluida"])
    id_parametro: int = Field(..., examples=[12])
    nome_parametro: str = Field(..., examples=["Cloro Residual Livre"])
    categoria: str | None = Field(default=None, examples=["Desinfeccao"])
    valor_resultado: float = Field(..., examples=[0.8])
    unidade_medida: str | None = Field(default=None, examples=["mg/L"])
    data_analise: date = Field(..., examples=["2026-04-03"])
    metodo_analise: str | None = Field(default=None, examples=["Metodo colorimetrico"])
    id_limite: int | None = Field(default=None, examples=[47])
    valor_minimo: float | None = Field(default=None, examples=[0.2])
    valor_maximo: float | None = Field(default=None, examples=[2.0])
    referencia_normativa: str | None = Field(default=None, examples=["Portaria GM/MS 888/2021"])
    classificacao_resultado: str = Field(..., examples=["Conforme"])
    possui_limite_referencia: bool = Field(..., examples=[True])
    indicador_nao_conforme: bool | None = Field(default=None, examples=[False])

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):
    page: int = Field(..., ge=1, examples=[1])
    page_size: int = Field(..., ge=1, le=100, examples=[20])
    total: int = Field(..., ge=0, examples=[72])


class ResultadoListResponse(BaseModel):
    success: bool = Field(default=True, examples=[True])
    message: str = Field(default="Consulta realizada com sucesso.")
    data: list[ResultadoResponse]
    pagination: PaginationResponse


class ResumoMensalResponse(BaseModel):
    ano_coleta: int | None = Field(default=None, examples=[2026])
    mes_coleta: int | None = Field(default=None, ge=1, le=12, examples=[4])
    total_resultados: int | None = Field(default=None, ge=0, examples=[72])
    resultados_com_limite: int | None = Field(default=None, ge=0, examples=[57])
    resultados_sem_limite: int | None = Field(default=None, ge=0, examples=[15])
    resultados_conformes_com_limite: int | None = Field(default=None, ge=0, examples=[50])
    resultados_nao_conformes_com_limite: int | None = Field(default=None, ge=0, examples=[7])
    percentual_conformidade_com_limite: float | None = Field(default=None, examples=[87.72])

    model_config = ConfigDict(from_attributes=True)


class ResumoMensalListResponse(BaseModel):
    success: bool = Field(default=True, examples=[True])
    message: str = Field(default="Consulta realizada com sucesso.")
    data: list[ResumoMensalResponse]
    pagination: PaginationResponse
