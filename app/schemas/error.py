from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., examples=["VALIDATION_ERROR"])
    details: str = Field(..., examples=["Parametro invalido na requisicao."])


class ErrorResponse(BaseModel):
    success: bool = Field(default=False, examples=[False])
    message: str = Field(..., examples=["Erro de validacao na requisicao."])
    error: ErrorDetail
