"""Schemas Pydantic (contratos de entrada/saida da API) para Faixa."""
from pydantic import BaseModel, ConfigDict


class FaixaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    latitude_a: float
    longitude_a: float
    latitude_b: float
    longitude_b: float
    executada: bool


class FaixaAtualizarEstado(BaseModel):
    executada: bool


class LinhaRejeitada(BaseModel):
    numero_linha: int
    conteudo: str
    motivo: str


class ResultadoImportacao(BaseModel):
    projeto_id: int
    faixas_importadas: list[FaixaResumo]
    linhas_rejeitadas: list[LinhaRejeitada]
    mensagem: str