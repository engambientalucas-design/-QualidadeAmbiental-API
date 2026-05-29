from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.error import DEFAULT_ERROR_RESPONSES
from app.schemas.resultados import (
    ParametroCriticoListResponse,
    ResultadoListResponse,
    ResumoMensalListResponse,
)
from app.services import resultados_service
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(
    prefix=f"{settings.API_V1_PREFIX}/resultados",
    tags=["resultados"],
)


@router.get(
    "/parametros-criticos",
    response_model=ParametroCriticoListResponse,
    summary="Lista ranking de parametros criticos",
    description="Consulta ranking de parametros criticos a partir da view VW_RankingParametrosCriticos.",
    responses=DEFAULT_ERROR_RESPONSES,
)
def list_parametros_criticos(
    categoria: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por categoria do parametro."),
    ] = None,
    limit: Annotated[
        int | None,
        Query(ge=1, le=MAX_PAGE_SIZE, description="Limita o ranking aos primeiros N parametros."),
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
    return resultados_service.list_parametros_criticos(
        db,
        categoria=categoria,
        limit=limit,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/resumo-mensal",
    response_model=ResumoMensalListResponse,
    summary="Lista resumo mensal de conformidade",
    description="Consulta indicadores mensais consolidados pela view VW_ConformidadeMensal.",
    responses=DEFAULT_ERROR_RESPONSES,
)
def list_resumo_mensal(
    ano: Annotated[
        int | None,
        Query(ge=2000, le=2100, description="Filtra por ano da coleta."),
    ] = None,
    mes: Annotated[
        int | None,
        Query(ge=1, le=12, description="Filtra por mes da coleta."),
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
    return resultados_service.list_resumo_mensal(
        db,
        ano=ano,
        mes=mes,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/sem-limite-referencia",
    response_model=ResultadoListResponse,
    summary="Lista resultados sem limite de referencia",
    description="Consulta resultados sem limite de referencia a partir da view VW_ResultadosSemLimiteReferencia.",
    responses=DEFAULT_ERROR_RESPONSES,
)
def list_resultados_sem_limite_referencia(
    data_inicio: Annotated[
        date | None,
        Query(description="Filtra coletas a partir desta data."),
    ] = None,
    data_fim: Annotated[
        date | None,
        Query(description="Filtra coletas ate esta data."),
    ] = None,
    municipio: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Filtra por municipio."),
    ] = None,
    id_ponto_coleta: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do ponto de coleta."),
    ] = None,
    id_parametro: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do parametro."),
    ] = None,
    categoria: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por categoria do parametro."),
    ] = None,
    codigo_amostra: Annotated[
        str | None,
        Query(min_length=1, max_length=50, description="Filtra por codigo da amostra."),
    ] = None,
    id_amostra: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador da amostra."),
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
    return resultados_service.list_resultados_sem_limite_referencia(
        db,
        data_inicio=data_inicio,
        data_fim=data_fim,
        municipio=municipio,
        id_ponto_coleta=id_ponto_coleta,
        id_parametro=id_parametro,
        categoria=categoria,
        codigo_amostra=codigo_amostra,
        id_amostra=id_amostra,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/nao-conformidades",
    response_model=ResultadoListResponse,
    summary="Lista resultados fora do padrao",
    description="Consulta resultados nao conformes a partir da view VW_ResultadosForaDoPadrao.",
    responses=DEFAULT_ERROR_RESPONSES,
)
def list_resultados_nao_conformidades(
    data_inicio: Annotated[
        date | None,
        Query(description="Filtra coletas a partir desta data."),
    ] = None,
    data_fim: Annotated[
        date | None,
        Query(description="Filtra coletas ate esta data."),
    ] = None,
    municipio: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Filtra por municipio."),
    ] = None,
    id_ponto_coleta: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do ponto de coleta."),
    ] = None,
    id_parametro: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do parametro."),
    ] = None,
    categoria: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por categoria do parametro."),
    ] = None,
    classificacao_resultado: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por classificacao calculada na view."),
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
    return resultados_service.list_resultados_nao_conformidades(
        db,
        data_inicio=data_inicio,
        data_fim=data_fim,
        municipio=municipio,
        id_ponto_coleta=id_ponto_coleta,
        id_parametro=id_parametro,
        categoria=categoria,
        classificacao_resultado=classificacao_resultado,
        page=page,
        page_size=page_size,
    )


@router.get(
    "",
    response_model=ResultadoListResponse,
    summary="Lista resultados analiticos consolidados",
    description="Consulta resultados consolidados pela view VW_ConformidadeResultados.",
    responses=DEFAULT_ERROR_RESPONSES,
)
def list_resultados(
    data_inicio: Annotated[
        date | None,
        Query(description="Filtra coletas a partir desta data."),
    ] = None,
    data_fim: Annotated[
        date | None,
        Query(description="Filtra coletas ate esta data."),
    ] = None,
    id_amostra: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador da amostra."),
    ] = None,
    codigo_amostra: Annotated[
        str | None,
        Query(min_length=1, max_length=50, description="Filtra por codigo da amostra."),
    ] = None,
    id_ponto_coleta: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do ponto de coleta."),
    ] = None,
    municipio: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Filtra por municipio."),
    ] = None,
    id_parametro: Annotated[
        int | None,
        Query(ge=1, description="Filtra por identificador do parametro."),
    ] = None,
    categoria: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por categoria do parametro."),
    ] = None,
    classificacao_resultado: Annotated[
        str | None,
        Query(min_length=1, max_length=80, description="Filtra por classificacao calculada na view."),
    ] = None,
    possui_limite_referencia: Annotated[
        bool | None,
        Query(description="Filtra resultados com ou sem limite de referencia."),
    ] = None,
    indicador_nao_conforme: Annotated[
        bool | None,
        Query(description="Filtra resultados conformes ou nao conformes quando ha limite."),
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
    return resultados_service.list_resultados(
        db,
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_amostra=id_amostra,
        codigo_amostra=codigo_amostra,
        id_ponto_coleta=id_ponto_coleta,
        municipio=municipio,
        id_parametro=id_parametro,
        categoria=categoria,
        classificacao_resultado=classificacao_resultado,
        possui_limite_referencia=possui_limite_referencia,
        indicador_nao_conforme=indicador_nao_conforme,
        page=page,
        page_size=page_size,
    )
