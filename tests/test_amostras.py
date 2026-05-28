from collections.abc import Generator
from datetime import date
from typing import Any

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.routers import amostras


client = TestClient(app)


def override_get_db() -> Generator[object, None, None]:
    yield object()


def test_amostras_returns_standard_response(monkeypatch) -> None:
    def fake_list_amostras(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [
                {
                    "id_amostra": 1,
                    "codigo_amostra": "AM-2026-001",
                    "data_coleta": "2026-04-01",
                    "hora_coleta": "08:30:00",
                    "id_ponto_coleta": 1,
                    "nome_ponto": "Captacao Rio Norte",
                    "municipio": "Cuiaba",
                    "estado": "MT",
                    "id_tipo_amostra": 1,
                    "nome_tipo_amostra": "Agua Bruta",
                    "id_status": 1,
                    "nome_status": "Coletada",
                    "id_responsavel": 1,
                    "nome_responsavel": "Maria Silva",
                    "observacao": "Coleta realizada sem intercorrencias.",
                }
            ],
            "pagination": {"page": 1, "page_size": 20, "total": 1},
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(amostras.amostras_service, "list_amostras", fake_list_amostras)

    response = client.get("/api/v1/amostras")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "Consulta realizada com sucesso."
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["id_amostra"] == 1
    assert payload["data"][0]["codigo_amostra"] == "AM-2026-001"
    assert payload["data"][0]["hora_coleta"] == "08:30:00"


def test_amostras_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_amostras(db: object, **kwargs: Any) -> dict:
        captured.update(kwargs)
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [],
            "pagination": {
                "page": kwargs["page"],
                "page_size": kwargs["page_size"],
                "total": 0,
            },
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(amostras.amostras_service, "list_amostras", fake_list_amostras)

    response = client.get(
        "/api/v1/amostras",
        params={
            "data_inicio": "2026-04-01",
            "data_fim": "2026-04-30",
            "id_ponto_coleta": 1,
            "municipio": "Cuiaba",
            "id_tipo_amostra": 2,
            "id_status": 3,
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "data_inicio": date(2026, 4, 1),
        "data_fim": date(2026, 4, 30),
        "id_ponto_coleta": 1,
        "municipio": "Cuiaba",
        "id_tipo_amostra": 2,
        "id_status": 3,
        "page": 2,
        "page_size": 10,
    }
    assert response.json()["pagination"] == {"page": 2, "page_size": 10, "total": 0}


def test_amostras_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/amostras", params={"page_size": 101})

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_amostras_rejects_invalid_date_range() -> None:
    response = client.get(
        "/api/v1/amostras",
        params={"data_inicio": "2026-04-30", "data_fim": "2026-04-01"},
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Erro ao processar a requisicao."
    assert payload["error"] == {
        "code": "HTTP_ERROR",
        "details": "data_inicio deve ser menor ou igual a data_fim.",
    }


def test_amostras_openapi_contains_endpoint_and_query_params() -> None:
    schema = app.openapi()
    operation = schema["paths"]["/api/v1/amostras"]["get"]
    params = [param["name"] for param in operation["parameters"]]

    assert operation["tags"] == ["amostras"]
    assert params == [
        "data_inicio",
        "data_fim",
        "id_ponto_coleta",
        "municipio",
        "id_tipo_amostra",
        "id_status",
        "page",
        "page_size",
    ]
