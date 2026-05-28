from sqlalchemy.orm import Session

from app.repositories import pontos_coleta_repository
from app.utils.pagination import pagination_metadata
from app.utils.responses import success_response


def list_pontos_coleta(
    db: Session,
    *,
    municipio: str | None = None,
    estado: str | None = None,
    tipo_ponto: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    normalized_estado = estado.upper() if estado else None

    data, total = pontos_coleta_repository.list_pontos_coleta(
        db,
        municipio=municipio,
        estado=normalized_estado,
        tipo_ponto=tipo_ponto,
        page=page,
        page_size=page_size,
    )

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )
