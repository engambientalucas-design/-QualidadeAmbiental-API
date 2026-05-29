from collections.abc import Iterable

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

PAGINATED_ENDPOINTS = [
    "/api/v1/pontos-coleta",
    "/api/v1/parametros",
    "/api/v1/amostras",
    "/api/v1/resultados",
    "/api/v1/resultados/nao-conformidades",
    "/api/v1/resultados/sem-limite-referencia",
    "/api/v1/resultados/resumo-mensal",
    "/api/v1/resultados/parametros-criticos",
]

EXPECTED_OPENAPI_PARAMS = {
    "/api/v1/pontos-coleta": ["municipio", "estado", "tipo_ponto", "page", "page_size"],
    "/api/v1/parametros": ["categoria", "ativo", "page", "page_size"],
    "/api/v1/amostras": [
        "data_inicio",
        "data_fim",
        "id_ponto_coleta",
        "municipio",
        "id_tipo_amostra",
        "id_status",
        "page",
        "page_size",
    ],
    "/api/v1/resultados": [
        "data_inicio",
        "data_fim",
        "id_amostra",
        "codigo_amostra",
        "id_ponto_coleta",
        "municipio",
        "id_parametro",
        "categoria",
        "classificacao_resultado",
        "possui_limite_referencia",
        "indicador_nao_conforme",
        "page",
        "page_size",
    ],
    "/api/v1/resultados/nao-conformidades": [
        "data_inicio",
        "data_fim",
        "municipio",
        "id_ponto_coleta",
        "id_parametro",
        "categoria",
        "classificacao_resultado",
        "page",
        "page_size",
    ],
    "/api/v1/resultados/sem-limite-referencia": [
        "data_inicio",
        "data_fim",
        "municipio",
        "id_ponto_coleta",
        "id_parametro",
        "categoria",
        "codigo_amostra",
        "id_amostra",
        "page",
        "page_size",
    ],
    "/api/v1/resultados/resumo-mensal": ["ano", "mes", "page", "page_size"],
    "/api/v1/resultados/parametros-criticos": ["categoria", "limit", "page", "page_size"],
}


def assert_validation_error(payload: dict) -> None:
    assert payload == {
        "success": False,
        "message": "Erro de validacao na requisicao.",
        "error": {
            "code": "VALIDATION_ERROR",
            "details": "Verifique os parametros enviados na requisicao.",
        },
    }


@pytest.mark.parametrize("path", PAGINATED_ENDPOINTS)
def test_paginated_endpoints_reject_page_size_above_limit(path: str) -> None:
    response = client.get(path, params={"page_size": 101})

    assert response.status_code == 422
    assert_validation_error(response.json())


@pytest.mark.parametrize("path", PAGINATED_ENDPOINTS)
def test_paginated_endpoints_reject_page_zero(path: str) -> None:
    response = client.get(path, params={"page": 0})

    assert response.status_code == 422
    assert_validation_error(response.json())


@pytest.mark.parametrize(
    ("path", "params"),
    [
        ("/api/v1/parametros", {"ativo": "talvez"}),
        ("/api/v1/resultados", {"possui_limite_referencia": "talvez"}),
        ("/api/v1/resultados", {"indicador_nao_conforme": "talvez"}),
        ("/api/v1/amostras", {"data_inicio": "2026-99-99"}),
        ("/api/v1/resultados/resumo-mensal", {"mes": 13}),
        ("/api/v1/resultados/parametros-criticos", {"limit": 101}),
    ],
)
def test_invalid_query_params_return_standard_validation_error(path: str, params: dict) -> None:
    response = client.get(path, params=params)

    assert response.status_code == 422
    assert_validation_error(response.json())


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/amostras",
        "/api/v1/resultados",
        "/api/v1/resultados/nao-conformidades",
        "/api/v1/resultados/sem-limite-referencia",
    ],
)
def test_invalid_date_range_returns_standard_http_error(path: str) -> None:
    response = client.get(
        path,
        params={"data_inicio": "2026-04-30", "data_fim": "2026-04-01"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Erro ao processar a requisicao.",
        "error": {
            "code": "HTTP_ERROR",
            "details": "data_inicio deve ser menor ou igual a data_fim.",
        },
    }


def test_openapi_lists_all_public_endpoints_and_query_params() -> None:
    schema = app.openapi()

    for path, expected_params in EXPECTED_OPENAPI_PARAMS.items():
        assert path in schema["paths"]
        operation = schema["paths"][path]["get"]
        assert operation["tags"]
        assert operation["summary"]
        assert operation["description"]
        assert [param["name"] for param in operation["parameters"]] == expected_params


def test_openapi_documents_standard_error_responses_for_paginated_endpoints() -> None:
    schema = app.openapi()

    for path in PAGINATED_ENDPOINTS:
        responses = schema["paths"][path]["get"]["responses"]
        assert "422" in responses
        assert "500" in responses
        assert (
            responses["422"]["content"]["application/json"]["schema"]["$ref"]
            == "#/components/schemas/ErrorResponse"
        )


def test_openapi_lists_expected_tags() -> None:
    schema = app.openapi()
    tags: Iterable[str] = (
        operation["tags"][0]
        for path_item in schema["paths"].values()
        for operation in path_item.values()
    )

    assert set(tags) == {"health", "pontos de coleta", "parametros", "amostras", "resultados"}
