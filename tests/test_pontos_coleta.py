from collections.abc import Generator
from typing import Any

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.routers import pontos_coleta


client = TestClient(app)


def override_get_db() -> Generator[object, None, None]:
    yield object()


def test_pontos_coleta_returns_standard_response(monkeypatch) -> None:
    def fake_list_pontos_coleta(db: object, **kwargs: Any) -> dict:
        return {
            "success": True,
            "message": "Consulta realizada com sucesso.",
            "data": [
                {
                    "id_ponto_coleta": 1,
                    "nome_ponto": "Rio Cuiaba - Ponto 01",
                    "tipo_ponto": "Corpo Hidrico",
                    "municipio": "Cuiaba",
                    "estado": "MT",
                    "latitude": None,
                    "longitude": None,
                    "observacao": "Ponto de monitoramento ambiental.",
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
        pontos_coleta.pontos_coleta_service,
        "list_pontos_coleta",
        fake_list_pontos_coleta,
    )

    response = client.get("/api/v1/pontos-coleta")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "Consulta realizada com sucesso."
    assert payload["pagination"] == {"page": 1, "page_size": 20, "total": 1}
    assert payload["data"][0]["id_ponto_coleta"] == 1
    assert payload["data"][0]["nome_ponto"] == "Rio Cuiaba - Ponto 01"


def test_pontos_coleta_forwards_filters_and_pagination(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def fake_list_pontos_coleta(db: object, **kwargs: Any) -> dict:
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
        pontos_coleta.pontos_coleta_service,
        "list_pontos_coleta",
        fake_list_pontos_coleta,
    )

    response = client.get(
        "/api/v1/pontos-coleta",
        params={
            "municipio": "Cuiaba",
            "estado": "mt",
            "tipo_ponto": "Corpo Hidrico",
            "page": 2,
            "page_size": 10,
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "municipio": "Cuiaba",
        "estado": "mt",
        "tipo_ponto": "Corpo Hidrico",
        "page": 2,
        "page_size": 10,
    }
    assert response.json()["pagination"] == {"page": 2, "page_size": 10, "total": 0}


def test_pontos_coleta_rejects_invalid_page_size() -> None:
    response = client.get("/api/v1/pontos-coleta", params={"page_size": 101})

    assert response.status_code == 422
