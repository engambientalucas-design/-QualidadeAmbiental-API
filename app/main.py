from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.config import settings
from app.routers import amostras, health, parametros, pontos_coleta, resultados


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(health.router)
    app.include_router(pontos_coleta.router)
    app.include_router(parametros.router)
    app.include_router(amostras.router)
    app.include_router(resultados.router)
    register_exception_handlers(app)

    return app


app = create_app()
