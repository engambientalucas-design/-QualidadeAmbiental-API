from fastapi import FastAPI

from app.core.config import settings
from app.routers import health, pontos_coleta


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(health.router)
    app.include_router(pontos_coleta.router)

    return app


app = create_app()
