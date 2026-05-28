from collections.abc import Generator
from typing import Any

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.routers import parametros


client = TestClient(app)


def override_get_db() -> Generator[object, None, None]:
    yield object()


def test_parametros_returns_standard_response(monkeypatch) -> None:
    def fake_list_parametros(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [
                {
                    "id_parametro": 1,
                    "nome_parametro": "Turbidez",
                    "unidade_medida": "NTU",
                    "categoria": "Fisico-quimico",
                    "descricao": "Parametro de qualidade da agua.",
                    "ativo": True,
                }
            ],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total": 1,
            },
        }

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        parametros.parametros_service,
        "list_parametros",
        fake_list_parametros,
    )

    response = client.get("/api/v1/parametros")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "Consulta realizada com sucesso."
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["id_parametro"] == 1
    assert payload["data"][0]["nome_parametro"] == "Turbidez"
    assert payload["data"][0]["ativo"] is True


def test_parametros_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_parametros(db: object, **kwargs: Any) -> dict:
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
    monkeypatch.setattr(
        parametros.parametros_service,
        "list_parametros",
        fake_list_parametros,
    )

    response = client.get(
        "/api/v1/parametros",
        params={
            "categoria": "Fisico-quimico",
            "ativo": "true",
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "categoria": "Fisico-quimico",
        "ativo": True,
        "page": 2,
        "page_size": 10,
    }
    assert response.json()["pagination"] == {"page": 2, "page_size": 10, "total": 0}


def test_parametros_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/parametros", params={"page_size": 101})

    assert response.status_code == 422
