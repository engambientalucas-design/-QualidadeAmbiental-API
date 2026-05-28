from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, calculate_offset


BASE_SELECT = """
    FROM Tbl_PontosColeta
    WHERE 1 = 1
"""


def _build_filters(
    municipio: str | None,
    estado: str | None,
    tipo_ponto: str | None,
) -> tuple[str, dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if municipio:
        conditions.append("AND Municipio = :municipio")
        params["municipio"] = municipio

    if estado:
        conditions.append("AND Estado = :estado")
        params["estado"] = estado

    if tipo_ponto:
        conditions.append("AND TipoPonto = :tipo_ponto")
        params["tipo_ponto"] = tipo_ponto

    return "\n".join(conditions), params


def list_pontos_coleta(
    db: Session,
    *,
    municipio: str | None = None,
    estado: str | None = None,
    tipo_ponto: str | None = None,
    page: int = DEFAULT_PAGE,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> tuple[list[dict[str, Any]], int]:
    filters_sql, params = _build_filters(municipio, estado, tipo_ponto)
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
            IdPontoColeta AS id_ponto_coleta,
            NomePonto AS nome_ponto,
            TipoPonto AS tipo_ponto,
            Municipio AS municipio,
            Estado AS estado,
            Latitude AS latitude,
            Longitude AS longitude,
            Observacao AS observacao
        {BASE_SELECT}
        {filters_sql}
        ORDER BY IdPontoColeta
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
