from fastapi import FastAPI

from app.core.config import settings
from app.routers import health


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(health.router)

    return app


app = create_app()
