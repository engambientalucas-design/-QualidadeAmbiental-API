from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.pontos_coleta import PontoColetaListResponse
from app.services import pontos_coleta_service
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/pontos-coleta",
    tags=["pontos de coleta"],
)


@router.get(
    "",
    response_model=PontoColetaListResponse,
    summary="Lista pontos de coleta",
    description="Consulta pontos de coleta cadastrados no SQL Server com filtros simples e paginação.",
)
def list_pontos_coleta(
    municipio: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Filtra por município."),
    ] = None,
    estado: Annotated[
        str | None,
        Query(min_length=2, max_length=2, description="Filtra por UF."),
    ] = None,
    tipo_ponto: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por tipo do ponto."),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1, description="Número da página."),
    ] = DEFAULT_PAGE,
    page_size: Annotated[
        int,
        Query(ge=1, le=MAX_PAGE_SIZE, description="Quantidade de registros por página."),
    ] = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db),
) -> dict:
    return pontos_coleta_service.list_pontos_coleta(
        db,
        municipio=municipio,
        estado=estado,
        tipo_ponto=tipo_ponto,
        page=page,
        page_size=page_size,
    )
