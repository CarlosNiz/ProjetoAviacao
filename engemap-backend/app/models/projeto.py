"""Modelo ORM da entidade Projeto."""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Projeto(Base):
    """Uma missao: agrupa um conjunto de faixas a serem executadas por uma aeronave."""

    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    faixas: Mapped[list["Faixa"]] = relationship(
        back_populates="projeto", cascade="all, delete-orphan"
    )