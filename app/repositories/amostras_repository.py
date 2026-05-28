from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, calculate_offset


BASE_SELECT = """
    FROM Tbl_Amostras AS a
    INNER JOIN Tbl_PontosColeta AS pc
        ON pc.IdPontoColeta = a.IdPontoColeta
    INNER JOIN Tbl_TiposAmostra AS ta
        ON ta.IdTipoAmostra = a.IdTipoAmostra
    INNER JOIN Tbl_StatusAmostra AS sa
        ON sa.IdStatus = a.IdStatus
    INNER JOIN Tbl_Responsaveis AS r
        ON r.IdResponsavel = a.IdResponsavel
    WHERE 1 = 1
"""


def _build_filters(
    data_inicio: date | None,
    data_fim: date | None,
    id_ponto_coleta: int | None,
    municipio: str | None,
    id_tipo_amostra: int | None,
    id_status: int | None,
) -> tuple[str, dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if data_inicio:
        conditions.append("AND a.DataColeta >= :data_inicio")
        params["data_inicio"] = data_inicio

    if data_fim:
        conditions.append("AND a.DataColeta <= :data_fim")
        params["data_fim"] = data_fim

    if id_ponto_coleta is not None:
        conditions.append("AND a.IdPontoColeta = :id_ponto_coleta")
        params["id_ponto_coleta"] = id_ponto_coleta

    if municipio:
        conditions.append("AND pc.Municipio = :municipio")
        params["municipio"] = municipio

    if id_tipo_amostra is not None:
        conditions.append("AND a.IdTipoAmostra = :id_tipo_amostra")
        params["id_tipo_amostra"] = id_tipo_amostra

    if id_status is not None:
        conditions.append("AND a.IdStatus = :id_status")
        params["id_status"] = id_status

    return "\n".join(conditions), params


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
) -> tuple[list[dict[str, Any]], int]:
    filters_sql, params = _build_filters(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_ponto_coleta=id_ponto_coleta,
        municipio=municipio,
        id_tipo_amostra=id_tipo_amostra,
        id_status=id_status,
    )
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
            a.IdAmostra AS id_amostra,
            a.CodigoAmostra AS codigo_amostra,
            a.DataColeta AS data_coleta,
            a.HoraColeta AS hora_coleta,
            a.IdPontoColeta AS id_ponto_coleta,
            pc.NomePonto AS nome_ponto,
            pc.Municipio AS municipio,
            pc.Estado AS estado,
            a.IdTipoAmostra AS id_tipo_amostra,
            ta.NomeTipoAmostra AS nome_tipo_amostra,
            a.IdStatus AS id_status,
            sa.NomeStatus AS nome_status,
            a.IdResponsavel AS id_responsavel,
            r.NomeResponsavel AS nome_responsavel,
            a.Observacao AS observacao
        {BASE_SELECT}
        {filters_sql}
        ORDER BY a.DataColeta DESC, a.IdAmostra DESC
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
