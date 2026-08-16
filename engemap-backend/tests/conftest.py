"""
Fixtures compartilhadas pelos testes automatizados.

Os testes usam SQLite em memoria em vez de PostgreSQL para serem rapidos e
independentes de infraestrutura externa (principio F.I.R.S.T). Nenhuma regra
de negocio testada aqui depende de recursos especificos do PostgreSQL.
"""
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401  (garante que Projeto e Faixa sejam registrados)
from app.database import Base


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()