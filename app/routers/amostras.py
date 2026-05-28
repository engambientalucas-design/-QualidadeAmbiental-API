from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.amostras import AmostraListResponse
from app.services import amostras_service
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/amostras",
    tags=["amostras"],
)


@router.get(
    "",
    response_model=AmostraListResponse,
    summary="Lista amostras",
    description="Consulta amostras com dados de ponto, tipo, status e responsavel.",
)
def list_amostras(
    data_inicio: Annotated[
        date | None,
        Query(description="Filtra coletas a partir desta data."),
    ] = None,
    data_fim: Annotated[
        date | None,
        Query(description="Filtra coletas ate esta data."),
    ] = None,
    id_ponto_coleta: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do ponto de coleta."),
    ] = None,
    municipio: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Filtra por municipio."),
    ] = None,
    id_tipo_amostra: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do tipo de amostra."),
    ] = None,
    id_status: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do status da amostra."),
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
    return amostras_service.list_amostras(
        db,
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_ponto_coleta=id_ponto_coleta,
        municipio=municipio,
        id_tipo_amostra=id_tipo_amostra,
        id_status=id_status,
        page=page,
        page_size=page_size,
    )
