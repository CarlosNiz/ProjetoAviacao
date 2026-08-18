"""Schemas Pydantic (contratos de entrada/saida da API) para Projeto."""
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.faixa import FaixaResumo


class ProjetoCriar(BaseModel):
    numero: int = Field(gt=0)
    nome: str = Field(min_length=1, max_length=64)


class ProjetoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero: int
    nome: str


class ProjetoDetalhe(ProjetoResumo):
    faixas: list[FaixaResumo] = []