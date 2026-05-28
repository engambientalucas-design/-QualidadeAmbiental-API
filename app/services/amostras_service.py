from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import amostras_repository
from app.utils.pagination import pagination_metadata
from app.utils.responses import success_response


def list_amostras(
    db: Session,
    *,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    id_ponto_coleta: int | None = None,
    municipio: str | None = None,
    id_tipo_amostra: int | None = None,
    id_status: int | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )

    data, total = amostras_repository.list_amostras(
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

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )
