"""Modelo ORM da entidade Faixa."""
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Faixa(Base):
    """Um conjunto de coordenadas (A -> B) a ser executado por uma aeronave."""

    __tablename__ = "faixas"
    __table_args__ = (
        UniqueConstraint("projeto_id", "nome", name="uq_faixa_nome_por_projeto"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(64), nullable=False)
    latitude_a: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_a: Mapped[float] = mapped_column(Float, nullable=False)
    latitude_b: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_b: Mapped[float] = mapped_column(Float, nullable=False)
    distancia_metros: Mapped[float] = mapped_column(Float, nullable=False)
    executada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    projeto: Mapped["Projeto"] = relationship(back_populates="faixas")