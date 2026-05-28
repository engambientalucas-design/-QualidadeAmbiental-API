from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.parametros import ParametroListResponse
from app.services import parametros_service

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/parametros",
    tags=["parametros"],
)


@router.get(
    "",
    response_model=ParametroListResponse,
    summary="Lista parametros ambientais",
    description="Consulta parametros ambientais cadastrados no SQL Server com filtros simples e paginacao.",
)
def list_parametros(
    categoria: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por categoria do parametro."),
    ] = None,
    ativo: Annotated[
        bool | None,
        Query(description="Filtra parametros ativos ou inativos."),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1, description="Numero da pagina."),
    ] = 1,
    page_size: Annotated[
        int,
        Query(ge=1, le=100, description="Quantidade de registros por pagina."),
    ] = 20,
    db: Session = Depends(get_db),
) -> dict:
    return parametros_service.list_parametros(
        db,
        categoria=categoria,
        ativo=ativo,
        page=page,
        page_size=page_size,
    )
