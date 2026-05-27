from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Verifica se a API está disponível")
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
