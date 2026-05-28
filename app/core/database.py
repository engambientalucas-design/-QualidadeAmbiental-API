from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings


def build_database_url() -> URL:
    query = {
        "driver": settings.DB_DRIVER,
        "Encrypt": settings.DB_ENCRYPT,
        "TrustServerCertificate": "yes" if settings.DB_TRUST_SERVER_CERTIFICATE else "no",
    }

    return URL.create(
        "mssql+pyodbc",
        username=settings.DB_USER or None,
        password=settings.DB_PASSWORD or None,
        host=settings.DB_SERVER,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        query=query,
    )


engine = create_engine(
    build_database_url(),
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
