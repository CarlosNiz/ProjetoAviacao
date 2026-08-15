"""Schemas Pydantic (contratos de entrada/saida da API) para Projeto."""
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.faixa import FaixaResumo


class ProjetoCriar(BaseModel):
    numero: str = Field(min_length=1, max_length=50)
    nome: str = Field(min_length=1, max_length=255)


class ProjetoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero: str
    nome: str


class ProjetoDetalhe(ProjetoResumo):
    faixas: list[FaixaResumo] = []