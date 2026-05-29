from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.error import DEFAULT_ERROR_RESPONSES
from app.schemas.parametros import ParametroListResponse
from app.services import parametros_service
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/parametros",
    tags=["parametros"],
)


@router.get(
    "",
    response_model=ParametroListResponse,
    summary="Lista parametros ambientais",
    description="Consulta parametros ambientais cadastrados no SQL Server com filtros simples e paginacao.",
    responses=DEFAULT_ERROR_RESPONSES,
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
    ] = DEFAULT_PAGE,
    page_size: Annotated[
        int,
        Query(ge=1, le=MAX_PAGE_SIZE, description="Quantidade de registros por pagina."),
    ] = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db),
) -> dict:
    return parametros_service.list_parametros(
        db,
        categoria=categoria,
        ativo=ativo,
        page=page,
        page_size=page_size,
    )
