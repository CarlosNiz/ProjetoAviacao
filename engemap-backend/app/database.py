"""Configuracao da conexao com o banco de dados via SQLAlchemy."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM do sistema."""


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessao de banco de dados por requisicao (dependency do FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()