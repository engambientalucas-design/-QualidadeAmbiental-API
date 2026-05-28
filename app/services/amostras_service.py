from datetime import date

from sqlalchemy.orm import Session

from app.repositories import amostras_repository
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, pagination_metadata
from app.utils.responses import success_response
from app.utils.validators import validate_date_range


def list_amostras(
    db: Session,
    *,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    id_ponto_coleta: int | None = None,
    municipio: str | None = None,
    id_tipo_amostra: int | None = None,
    id_status: int | None = None,
    page: int = DEFAULT_PAGE,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> dict:
    validate_date_range(data_inicio, data_fim)

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
