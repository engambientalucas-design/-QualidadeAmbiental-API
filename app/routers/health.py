from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.error import DEFAULT_ERROR_RESPONSES

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Verifica disponibilidade da API",
    description="Retorna status operacional basico da aplicacao, sem consultar o SQL Server.",
    responses={500: DEFAULT_ERROR_RESPONSES[500]},
)
def health_check() -> dict:
    return {
        "success": True,
        "message": "API disponível.",
        "data": {
            "status": "ok",
            "service": settings.PROJECT_NAME,
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    }
