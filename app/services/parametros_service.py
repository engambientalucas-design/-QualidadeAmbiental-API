from sqlalchemy.orm import Session

from app.repositories import parametros_repository
from app.utils.pagination import pagination_metadata
from app.utils.responses import success_response


def list_parametros(
    db: Session,
    *,
    categoria: str | None = None,
    ativo: bool | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    data, total = parametros_repository.list_parametros(
        db,
        categoria=categoria,
        ativo=ativo,
        page=page,
        page_size=page_size,
    )

    return success_response(
        message="Consulta realizada com sucesso.",
        data=data,
        pagination=pagination_metadata(page=page, page_size=page_size, total=total),
    )
