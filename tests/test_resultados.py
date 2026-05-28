from collections.abc import Generator
from datetime import date
from typing import Any

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.routers import resultados


client = TestClient(app)


def override_get_db() -> Generator[object, None, None]:
    yield object()


def resultado_payload(indicador_nao_conforme: bool | None = False) -> dict[str, Any]:
    return {
        "id_resultado": 72,
        "id_amostra": 6,
        "codigo_amostra": "QA-2026-006",
        "data_coleta": "2026-04-03",
        "hora_coleta": "11:15:00",
        "id_tipo_amostra": 2,
        "nome_tipo_amostra": "Agua Tratada",
        "id_ponto_coleta": 6,
        "nome_ponto": "Reservatorio Bairro Leste",
        "tipo_ponto": "Reservatorio",
        "municipio": "Cuiaba",
        "estado": "MT",
        "id_responsavel": 4,
        "nome_responsavel": "Joao Pereira",
        "id_status": 3,
        "nome_status": "Concluida",
        "id_parametro": 12,
        "nome_parametro": "Cloro Residual Livre",
        "categoria": "Desinfeccao",
        "valor_resultado": 0.8,
        "unidade_medida": "mg/L",
        "data_analise": "2026-04-03",
        "metodo_analise": "Metodo colorimetrico",
        "id_limite": 47,
        "valor_minimo": 0.2,
        "valor_maximo": 2.0,
        "referencia_normativa": "Portaria GM/MS 888/2021",
        "classificacao_resultado": "Conforme",
        "possui_limite_referencia": True,
        "indicador_nao_conforme": indicador_nao_conforme,
    }


def resumo_mensal_payload() -> dict[str, Any]:
    return {
        "ano_coleta": 2026,
        "mes_coleta": 4,
        "total_resultados": 72,
        "resultados_com_limite": 57,
        "resultados_sem_limite": 15,
        "resultados_conformes_com_limite": 50,
        "resultados_nao_conformes_com_limite": 7,
        "percentual_conformidade_com_limite": 87.72,
    }


def parametro_critico_payload() -> dict[str, Any]:
    return {
        "ranking": 1,
        "id_parametro": 2,
        "nome_parametro": "Turbidez",
        "categoria": "Fisico-quimico",
        "total_resultados": 6,
        "resultados_com_limite": 5,
        "resultados_sem_limite": 1,
        "total_nao_conformidades": 2,
        "percentual_nao_conformidade_com_limite": 40.0,
    }


def test_resultados_returns_standard_response(monkeypatch) -> None:
    def fake_list_resultados(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [resultado_payload()],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(resultados.resultados_service, "list_resultados", fake_list_resultados)

    response = client.get("/api/v1/resultados")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["valor_resultado"] == 0.8
    assert payload["data"][0]["possui_limite_referencia"] is True
    assert payload["data"][0]["indicador_nao_conforme"] is False


def test_resultados_accepts_null_indicador_nao_conforme(monkeypatch) -> None:
    def fake_list_resultados(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [resultado_payload(indicador_nao_conforme=None)],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(resultados.resultados_service, "list_resultados", fake_list_resultados)

    response = client.get("/api/v1/resultados")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["data"][0]["indicador_nao_conforme"] is None


def test_resultados_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_resultados(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {"page": kwargs["page"], "page_size": kwargs["page_size"], "total": 0},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(resultados.resultados_service, "list_resultados", fake_list_resultados)

    response = client.get(
        "/api/v1/resultados",
        params={
            "data_inicio": "2026-04-01",
            "data_fim": "2026-04-03",
            "id_amostra": 6,
            "codigo_amostra": "QA-2026-006",
            "id_ponto_coleta": 6,
            "municipio": "Cuiaba",
            "id_parametro": 11,
            "categoria": "Fisico-quimico",
            "classificacao_resultado": "Conforme",
            "possui_limite_referencia": "true",
            "indicador_nao_conforme": "false",
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "data_inicio": date(2026, 4, 1),
        "data_fim": date(2026, 4, 3),
        "id_amostra": 6,
        "codigo_amostra": "QA-2026-006",
        "id_ponto_coleta": 6,
        "municipio": "Cuiaba",
        "id_parametro": 11,
        "categoria": "Fisico-quimico",
        "classificacao_resultado": "Conforme",
        "possui_limite_referencia": True,
        "indicador_nao_conforme": False,
        "page": 2,
        "page_size": 10,
    }


def test_resultados_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/resultados", params={"page_size": 101})

    assert response.status_code == 422


def test_resultados_rejects_invalid_date_range() -> None:
    response = client.get(
        "/api/v1/resultados",
        params={"data_inicio": "2026-04-03", "data_fim": "2026-04-01"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "data_inicio deve ser menor ou igual a data_fim."


def test_resultados_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/resultados"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["resultados"]
    assert params == [
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
    ]


def test_resultados_nao_conformidades_returns_standard_response(monkeypatch) -> None:
    def fake_list_resultados_nao_conformidades(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [resultado_payload(indicador_nao_conforme=True)],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resultados_nao_conformidades",
        fake_list_resultados_nao_conformidades,
    )

    response = client.get("/api/v1/resultados/nao-conformidades")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["indicador_nao_conforme"] is True


def test_resultados_nao_conformidades_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_resultados_nao_conformidades(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {"page": kwargs["page"], "page_size": kwargs["page_size"], "total": 0},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resultados_nao_conformidades",
        fake_list_resultados_nao_conformidades,
    )

    response = client.get(
        "/api/v1/resultados/nao-conformidades",
        params={
            "data_inicio": "2026-04-01",
            "data_fim": "2026-04-03",
            "municipio": "Cuiaba",
            "id_ponto_coleta": 6,
            "id_parametro": 11,
            "categoria": "Nutrientes",
            "classificacao_resultado": "Acima do limite maximo",
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "data_inicio": date(2026, 4, 1),
        "data_fim": date(2026, 4, 3),
        "municipio": "Cuiaba",
        "id_ponto_coleta": 6,
        "id_parametro": 11,
        "categoria": "Nutrientes",
        "classificacao_resultado": "Acima do limite maximo",
        "page": 2,
        "page_size": 10,
    }


def test_resultados_nao_conformidades_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/resultados/nao-conformidades", params={"page_size": 101})

    assert response.status_code == 422


def test_resultados_nao_conformidades_rejects_invalid_date_range() -> None:
    response = client.get(
        "/api/v1/resultados/nao-conformidades",
        params={"data_inicio": "2026-04-03", "data_fim": "2026-04-01"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "data_inicio deve ser menor ou igual a data_fim."


def test_resultados_nao_conformidades_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/resultados/nao-conformidades"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["resultados"]
    assert params == [
        "data_inicio",
        "data_fim",
        "municipio",
        "id_ponto_coleta",
        "id_parametro",
        "categoria",
        "classificacao_resultado",
        "page",
        "page_size",
    ]


def test_resultados_sem_limite_referencia_returns_standard_response(monkeypatch) -> None:
    def fake_list_resultados_sem_limite_referencia(db: object, **kwargs: Any) -> dict:
        payload = resultado_payload(indicador_nao_conforme=None)
        payload["classificacao_resultado"] = "Sem limite de referencia"
        payload["possui_limite_referencia"] = False
        payload["id_limite"] = None
        payload["valor_minimo"] = None
        payload["valor_maximo"] = None
        payload["referencia_normativa"] = None
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [payload],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resultados_sem_limite_referencia",
        fake_list_resultados_sem_limite_referencia,
    )

    response = client.get("/api/v1/resultados/sem-limite-referencia")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["classificacao_resultado"] == "Sem limite de referencia"
    assert payload["data"][0]["possui_limite_referencia"] is False
    assert payload["data"][0]["indicador_nao_conforme"] is None


def test_resultados_sem_limite_referencia_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_resultados_sem_limite_referencia(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {"page": kwargs["page"], "page_size": kwargs["page_size"], "total": 0},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resultados_sem_limite_referencia",
        fake_list_resultados_sem_limite_referencia,
    )

    response = client.get(
        "/api/v1/resultados/sem-limite-referencia",
        params={
            "data_inicio": "2026-04-01",
            "data_fim": "2026-04-03",
            "municipio": "Cuiaba",
            "id_ponto_coleta": 6,
            "id_parametro": 4,
            "categoria": "Materia organica",
            "codigo_amostra": "QA-2026-006",
            "id_amostra": 6,
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "data_inicio": date(2026, 4, 1),
        "data_fim": date(2026, 4, 3),
        "municipio": "Cuiaba",
        "id_ponto_coleta": 6,
        "id_parametro": 4,
        "categoria": "Materia organica",
        "codigo_amostra": "QA-2026-006",
        "id_amostra": 6,
        "page": 2,
        "page_size": 10,
    }


def test_resultados_sem_limite_referencia_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/resultados/sem-limite-referencia", params={"page_size": 101})

    assert response.status_code == 422


def test_resultados_sem_limite_referencia_rejects_invalid_date_range() -> None:
    response = client.get(
        "/api/v1/resultados/sem-limite-referencia",
        params={"data_inicio": "2026-04-03", "data_fim": "2026-04-01"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "data_inicio deve ser menor ou igual a data_fim."


def test_resultados_sem_limite_referencia_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/resultados/sem-limite-referencia"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["resultados"]
    assert params == [
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
    ]


def test_resultados_resumo_mensal_returns_standard_response(monkeypatch) -> None:
    def fake_list_resumo_mensal(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [resumo_mensal_payload()],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resumo_mensal",
        fake_list_resumo_mensal,
    )

    response = client.get("/api/v1/resultados/resumo-mensal")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0] == resumo_mensal_payload()


def test_resultados_resumo_mensal_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_resumo_mensal(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {"page": kwargs["page"], "page_size": kwargs["page_size"], "total": 0},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_resumo_mensal",
        fake_list_resumo_mensal,
    )

    response = client.get(
        "/api/v1/resultados/resumo-mensal",
        params={"ano": 2026, "mes": 4, "page": 2, "page_size": 10},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {"ano": 2026, "mes": 4, "page": 2, "page_size": 10}


def test_resultados_resumo_mensal_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/resultados/resumo-mensal", params={"page_size": 101})

    assert response.status_code == 422


def test_resultados_resumo_mensal_rejects_invalid_mes() -> None:
    response = client.get("/api/v1/resultados/resumo-mensal", params={"mes": 13})

    assert response.status_code == 422


def test_resultados_resumo_mensal_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/resultados/resumo-mensal"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["resultados"]
    assert params == ["ano", "mes", "page", "page_size"]


def test_resultados_parametros_criticos_returns_standard_response(monkeypatch) -> None:
    def fake_list_parametros_criticos(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [parametro_critico_payload()],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_parametros_criticos",
        fake_list_parametros_criticos,
    )

    response = client.get("/api/v1/resultados/parametros-criticos")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0] == parametro_critico_payload()


def test_resultados_parametros_criticos_forwards_filters_limit_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_parametros_criticos(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {"page": kwargs["page"], "page_size": kwargs["page_size"], "total": 0},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        resultados.resultados_service,
        "list_parametros_criticos",
        fake_list_parametros_criticos,
    )

    response = client.get(
        "/api/v1/resultados/parametros-criticos",
        params={"categoria": "Fisico-quimico", "limit": 5, "page": 2, "page_size": 10},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "categoria": "Fisico-quimico",
        "limit": 5,
        "page": 2,
        "page_size": 10,
    }


def test_resultados_parametros_criticos_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/resultados/parametros-criticos", params={"page_size": 101})

    assert response.status_code == 422


def test_resultados_parametros_criticos_rejects_invalid_limit() -> None:
    response = client.get("/api/v1/resultados/parametros-criticos", params={"limit": 101})

    assert response.status_code == 422


def test_resultados_parametros_criticos_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/resultados/parametros-criticos"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["resultados"]
    assert params == ["categoria", "limit", "page", "page_size"]
