"""Calculo do progresso de execucao de um projeto a partir de suas faixas."""
from dataclasses import dataclass
from typing import Iterable

from app.models.faixa import Faixa


@dataclass
class ResumoDeExecucao:
    distancia_total_metros: float
    distancia_executada_metros: float
    percentual_executado: float
    faixas_executadas: int
    total_de_faixas: int


def calcular_resumo(faixas: Iterable[Faixa]) -> ResumoDeExecucao:
    """Soma as distancias planejadas e executadas e deriva o percentual de execucao."""
    faixas = list(faixas)
    distancia_total = sum(faixa.distancia_metros for faixa in faixas)
    distancia_executada = sum(faixa.distancia_metros for faixa in faixas if faixa.executada)

    # Projeto sem faixas nao tem distancia planejada; retornar 0 evita divisao
    # por zero e representa corretamente "nada executado".
    percentual = (distancia_executada / distancia_total * 100) if distancia_total > 0 else 0.0

    return ResumoDeExecucao(
        distancia_total_metros=distancia_total,
        distancia_executada_metros=distancia_executada,
        percentual_executado=percentual,
        faixas_executadas=sum(1 for faixa in faixas if faixa.executada),
        total_de_faixas=len(faixas),
    )