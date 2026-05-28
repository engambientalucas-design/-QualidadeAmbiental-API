from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.main import create_app


def test_unhandled_exception_returns_safe_error_response() -> None:
    app = create_app()
    router = APIRouter()

    @router.get("/boom")
    def boom() -> None:
        raise RuntimeError("sensitive internal detail")

    app.include_router(router)
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/boom")

    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "message": "Erro interno do servidor.",
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "details": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
        },
    }


def test_validation_error_response_does_not_expose_raw_fastapi_detail() -> None:
    app = create_app()
    router = APIRouter()

    @router.get("/items")
    def list_items(page_size: int) -> dict:
        return {"page_size": page_size}

    app.include_router(router)
    client = TestClient(app)

    response = client.get("/items", params={"page_size": "invalid"})

    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Erro de validacao na requisicao.",
        "error": {
            "code": "VALIDATION_ERROR",
            "details": "Verifique os parametros enviados na requisicao.",
        },
    }
