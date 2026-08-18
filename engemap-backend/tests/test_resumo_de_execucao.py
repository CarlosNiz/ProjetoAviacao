"""Testes do calculo de progresso de execucao do projeto."""
from app.models.faixa import Faixa
from app.services.resumo_de_execucao import calcular_resumo


def _faixa(distancia_metros: float, executada: bool) -> Faixa:
    return Faixa(
        nome="faixa",
        latitude_a=0.0,
        longitude_a=0.0,
        latitude_b=0.0,
        longitude_b=0.0,
        distancia_metros=distancia_metros,
        executada=executada,
    )


def test_projeto_sem_faixas_tem_percentual_zero() -> None:
    resumo = calcular_resumo([])

    assert resumo.distancia_total_metros == 0
    assert resumo.percentual_executado == 0.0


def test_soma_distancias_planejadas_e_executadas() -> None:
    faixas = [_faixa(60_000, executada=True), _faixa(40_000, executada=False)]

    resumo = calcular_resumo(faixas)

    assert resumo.distancia_total_metros == 100_000
    assert resumo.distancia_executada_metros == 60_000
    assert resumo.percentual_executado == 60.0


def test_projeto_totalmente_executado_tem_cem_por_cento() -> None:
    faixas = [_faixa(10_000, executada=True), _faixa(20_000, executada=True)]

    resumo = calcular_resumo(faixas)

    assert resumo.percentual_executado == 100.0


def test_contabiliza_quantidade_de_faixas() -> None:
    faixas = [_faixa(1_000, executada=True), _faixa(1_000, executada=False)]

    resumo = calcular_resumo(faixas)

    assert resumo.faixas_executadas == 1
    assert resumo.total_de_faixas == 2