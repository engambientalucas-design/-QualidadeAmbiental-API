from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


BASE_SELECT_RESULTADOS = """
    FROM VW_ConformidadeResultados
    WHERE 1 = 1
"""

BASE_SELECT_NAO_CONFORMIDADES = """
    FROM VW_ResultadosForaDoPadrao AS fp
    INNER JOIN VW_ConformidadeResultados AS cr
        ON cr.IdResultado = fp.IdResultado
    WHERE 1 = 1
"""


def _build_filters(
    data_inicio: date | None,
    data_fim: date | None,
    id_amostra: int | None,
    codigo_amostra: str | None,
    id_ponto_coleta: int | None,
    municipio: str | None,
    id_parametro: int | None,
    categoria: str | None,
    classificacao_resultado: str | None,
    possui_limite_referencia: bool | None,
    indicador_nao_conforme: bool | None,
) -> tuple[str, dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if data_inicio:
        conditions.append("AND DataColeta >= :data_inicio")
        params["data_inicio"] = data_inicio

    if data_fim:
        conditions.append("AND DataColeta <= :data_fim")
        params["data_fim"] = data_fim

    if id_amostra is not None:
        conditions.append("AND IdAmostra = :id_amostra")
        params["id_amostra"] = id_amostra

    if codigo_amostra:
        conditions.append("AND CodigoAmostra = :codigo_amostra")
        params["codigo_amostra"] = codigo_amostra

    if id_ponto_coleta is not None:
        conditions.append("AND IdPontoColeta = :id_ponto_coleta")
        params["id_ponto_coleta"] = id_ponto_coleta

    if municipio:
        conditions.append("AND Municipio = :municipio")
        params["municipio"] = municipio

    if id_parametro is not None:
        conditions.append("AND IdParametro = :id_parametro")
        params["id_parametro"] = id_parametro

    if categoria:
        conditions.append("AND Categoria = :categoria")
        params["categoria"] = categoria

    if classificacao_resultado:
        conditions.append("AND ClassificacaoResultado = :classificacao_resultado")
        params["classificacao_resultado"] = classificacao_resultado

    if possui_limite_referencia is not None:
        conditions.append("AND PossuiLimiteReferencia = :possui_limite_referencia")
        params["possui_limite_referencia"] = int(possui_limite_referencia)

    if indicador_nao_conforme is not None:
        conditions.append("AND IndicadorNaoConforme = :indicador_nao_conforme")
        params["indicador_nao_conforme"] = int(indicador_nao_conforme)

    return "\n".join(conditions), params


def _build_nao_conformidades_filters(
    data_inicio: date | None,
    data_fim: date | None,
    municipio: str | None,
    id_ponto_coleta: int | None,
    id_parametro: int | None,
    categoria: str | None,
    classificacao_resultado: str | None,
) -> tuple[str, dict[str, Any]]:
    conditions: list[str] = []
    params: dict[str, Any] = {}

    if data_inicio:
        conditions.append("AND cr.DataColeta >= :data_inicio")
        params["data_inicio"] = data_inicio

    if data_fim:
        conditions.append("AND cr.DataColeta <= :data_fim")
        params["data_fim"] = data_fim

    if municipio:
        conditions.append("AND cr.Municipio = :municipio")
        params["municipio"] = municipio

    if id_ponto_coleta is not None:
        conditions.append("AND cr.IdPontoColeta = :id_ponto_coleta")
        params["id_ponto_coleta"] = id_ponto_coleta

    if id_parametro is not None:
        conditions.append("AND cr.IdParametro = :id_parametro")
        params["id_parametro"] = id_parametro

    if categoria:
        conditions.append("AND cr.Categoria = :categoria")
        params["categoria"] = categoria

    if classificacao_resultado:
        conditions.append("AND cr.ClassificacaoResultado = :classificacao_resultado")
        params["classificacao_resultado"] = classificacao_resultado

    return "\n".join(conditions), params


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    return value


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {key: _normalize_value(value) for key, value in row.items()}
    normalized["possui_limite_referencia"] = bool(normalized["possui_limite_referencia"])

    indicador = normalized["indicador_nao_conforme"]
    normalized["indicador_nao_conforme"] = None if indicador is None else bool(indicador)

    return normalized


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
) -> tuple[list[dict[str, Any]], int]:
    filters_sql, params = _build_filters(
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
    )
    offset = (page - 1) * page_size

    count_query = text(
        f"""
        SELECT COUNT(1)
        {BASE_SELECT_RESULTADOS}
        {filters_sql}
        """
    )

    total = db.execute(count_query, params).scalar_one()

    list_query = text(
        f"""
        SELECT
            IdResultado AS id_resultado,
            IdAmostra AS id_amostra,
            CodigoAmostra AS codigo_amostra,
            DataColeta AS data_coleta,
            HoraColeta AS hora_coleta,
            IdTipoAmostra AS id_tipo_amostra,
            NomeTipoAmostra AS nome_tipo_amostra,
            IdPontoColeta AS id_ponto_coleta,
            NomePonto AS nome_ponto,
            TipoPonto AS tipo_ponto,
            Municipio AS municipio,
            Estado AS estado,
            IdResponsavel AS id_responsavel,
            NomeResponsavel AS nome_responsavel,
            IdStatus AS id_status,
            NomeStatus AS nome_status,
            IdParametro AS id_parametro,
            NomeParametro AS nome_parametro,
            Categoria AS categoria,
            ValorResultado AS valor_resultado,
            UnidadeMedida AS unidade_medida,
            DataAnalise AS data_analise,
            MetodoAnalise AS metodo_analise,
            IdLimite AS id_limite,
            ValorMinimo AS valor_minimo,
            ValorMaximo AS valor_maximo,
            ReferenciaNormativa AS referencia_normativa,
            ClassificacaoResultado AS classificacao_resultado,
            PossuiLimiteReferencia AS possui_limite_referencia,
            IndicadorNaoConforme AS indicador_nao_conforme
        {BASE_SELECT_RESULTADOS}
        {filters_sql}
        ORDER BY DataColeta DESC, IdAmostra DESC, IdResultado DESC
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

    return [_normalize_row(dict(row)) for row in rows], total


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
) -> tuple[list[dict[str, Any]], int]:
    filters_sql, params = _build_nao_conformidades_filters(
        data_inicio=data_inicio,
        data_fim=data_fim,
        municipio=municipio,
        id_ponto_coleta=id_ponto_coleta,
        id_parametro=id_parametro,
        categoria=categoria,
        classificacao_resultado=classificacao_resultado,
    )
    offset = (page - 1) * page_size

    count_query = text(
        f"""
        SELECT COUNT(1)
        {BASE_SELECT_NAO_CONFORMIDADES}
        {filters_sql}
        """
    )

    total = db.execute(count_query, params).scalar_one()

    list_query = text(
        f"""
        SELECT
            cr.IdResultado AS id_resultado,
            cr.IdAmostra AS id_amostra,
            cr.CodigoAmostra AS codigo_amostra,
            cr.DataColeta AS data_coleta,
            cr.HoraColeta AS hora_coleta,
            cr.IdTipoAmostra AS id_tipo_amostra,
            cr.NomeTipoAmostra AS nome_tipo_amostra,
            cr.IdPontoColeta AS id_ponto_coleta,
            cr.NomePonto AS nome_ponto,
            cr.TipoPonto AS tipo_ponto,
            cr.Municipio AS municipio,
            cr.Estado AS estado,
            cr.IdResponsavel AS id_responsavel,
            cr.NomeResponsavel AS nome_responsavel,
            cr.IdStatus AS id_status,
            cr.NomeStatus AS nome_status,
            cr.IdParametro AS id_parametro,
            cr.NomeParametro AS nome_parametro,
            cr.Categoria AS categoria,
            cr.ValorResultado AS valor_resultado,
            cr.UnidadeMedida AS unidade_medida,
            cr.DataAnalise AS data_analise,
            cr.MetodoAnalise AS metodo_analise,
            cr.IdLimite AS id_limite,
            cr.ValorMinimo AS valor_minimo,
            cr.ValorMaximo AS valor_maximo,
            cr.ReferenciaNormativa AS referencia_normativa,
            cr.ClassificacaoResultado AS classificacao_resultado,
            cr.PossuiLimiteReferencia AS possui_limite_referencia,
            cr.IndicadorNaoConforme AS indicador_nao_conforme
        {BASE_SELECT_NAO_CONFORMIDADES}
        {filters_sql}
        ORDER BY cr.DataColeta DESC, cr.IdAmostra DESC, cr.IdResultado DESC
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

    return [_normalize_row(dict(row)) for row in rows], total
