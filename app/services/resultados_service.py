from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import resultados_repository
from app.utils.pagination import pagination_metadata
from app.utils.responses import success_response


def list_resultados(
    db: Session,
    *,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    id_amostra: int | None = None,
    codigo_amostra: str | None = None,
    id_ponto_coleta: int | None = None,
    municipio: str | None = None,
    id_parametro: int | None = None,
    categoria: str | None = None,
    classificacao_resultado: str | None = None,
    possui_limite_referencia: bool | None = None,
    indicador_nao_conforme: bool | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )

    data, total = resultados_repository.list_resultados(
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

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )


def list_resultados_nao_conformidades(
    db: Session,
    *,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    municipio: str | None = None,
    id_ponto_coleta: int | None = None,
    id_parametro: int | None = None,
    categoria: str | None = None,
    classificacao_resultado: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )

    data, total = resultados_repository.list_resultados_nao_conformidades(
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

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )


def list_resultados_sem_limite_referencia(
    db: Session,
    *,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    municipio: str | None = None,
    id_ponto_coleta: int | None = None,
    id_parametro: int | None = None,
    categoria: str | None = None,
    codigo_amostra: str | None = None,
    id_amostra: int | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )

    data, total = resultados_repository.list_resultados_sem_limite_referencia(
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

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )
