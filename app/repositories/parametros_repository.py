from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, calculate_offset


BASE_SELECT = """
    FROM Tbl_Parametros
    WHERE 1 = 1
"""


def _build_filters(
    categoria: str | None,
    ativo: bool | None,
) -> tuple[str, dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if categoria:
        conditions.append("AND Categoria = :categoria")
        params["categoria"] = categoria

    if ativo is not None:
        conditions.append("AND Ativo = :ativo")
        params["ativo"] = ativo

    return "\n".join(conditions), params


def list_parametros(
    db: Session,
    *,
    categoria: str | None = None,
    ativo: bool | None = None,
    page: int = DEFAULT_PAGE,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> tuple[list[dict[str, Any]], int]:
    filters_sql, params = _build_filters(categoria, ativo)
    offset = calculate_offset(page=page, page_size=page_size)

    count_query = text(
        f"""
        SELECT COUNT(1)
        {BASE_SELECT}
        {filters_sql}
        """
    )

    total = db.execute(count_query, params).scalar_one()

    list_query = text(
        f"""
        SELECT
            IdParametro AS id_parametro,
            NomeParametro AS nome_parametro,
            UnidadeMedida AS unidade_medida,
            Categoria AS categoria,
            Descricao AS descricao,
            CAST(Ativo AS bit) AS ativo
        {BASE_SELECT}
        {filters_sql}
        ORDER BY IdParametro
        OFFSET :offset ROWS
        FETCH NEXT :page_size ROWS ONLY
        """
    )

    rows = db.execute(
        list_query,
        {
            **params,
            "offset": offset,
            "page_size": page_size,
        },
    ).mappings()

    return [dict(row) for row in rows], total
