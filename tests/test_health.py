from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_200() -> None:
    response = client.get("/health")

    assert response.status_code == 200


def test_health_response_contract() -> None:
    response = client.get("/health")
    payload = response.json()

    assert payload["success"] is True
    assert payload["message"] == "API disponível."
    assert payload["data"]["status"] == "ok"
    assert payload["data"]["service"]
    assert payload["data"]["version"]
    assert payload["data"]["environment"]
    assert payload["data"]["timestamp"]
