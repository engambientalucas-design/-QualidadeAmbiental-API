from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.utils.responses import error_response

logger = get_logger(__name__)


def _safe_details(detail: object) -> str:
    if isinstance(detail, str):
        return detail
    return "Verifique os parametros enviados na requisicao."


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.info(
        "request_validation_error path=%s errors=%s",
        request.url.path,
        exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Erro de validacao na requisicao.",
            code="VALIDATION_ERROR",
            details="Verifique os parametros enviados na requisicao.",
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.info(
        "http_exception path=%s status_code=%s detail=%s",
        request.url.path,
        exc.status_code,
        exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message="Erro ao processar a requisicao.",
            code="HTTP_ERROR",
            details=_safe_details(exc.detail),
        ),
        headers=exc.headers,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception path=%s", request.url.path)
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Erro interno do servidor.",
            code="INTERNAL_SERVER_ERROR",
            details="Ocorreu um erro inesperado. Tente novamente mais tarde.",
        ),
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
