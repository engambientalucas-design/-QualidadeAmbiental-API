from uuid import UUID

from fastapi.testclient import TestClient

from app.core.middleware import REQUEST_ID_HEADER
from app.main import app


client = TestClient(app)


def test_response_includes_generated_request_id() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    request_id = response.headers[REQUEST_ID_HEADER]
    assert UUID(request_id)
    assert response.json()["success"] is True


def test_response_preserves_client_request_id() -> None:
    request_id = "qa-api-test-request-id"

    response = client.get("/health", headers={REQUEST_ID_HEADER: request_id})

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id
    assert response.json()["data"]["status"] == "ok"


def test_validation_error_response_includes_request_id_header() -> None:
    response = client.get("/api/v1/resultados", params={"page_size": 101})

    assert response.status_code == 422
    assert UUID(response.headers[REQUEST_ID_HEADER])
    assert response.json()["success"] is False
