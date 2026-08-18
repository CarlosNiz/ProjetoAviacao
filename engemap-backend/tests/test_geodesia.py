"""Testes do calculo de distancia geografica."""
from app.services.geodesia import calcular_distancia_em_metros


def test_distancia_entre_pontos_identicos_e_zero() -> None:
    distancia = calcular_distancia_em_metros(-23.556677, -46.633088, -23.556677, -46.633088)

    assert distancia == 0.0


def test_distancia_conhecida_entre_sao_paulo_e_rio() -> None:
    # Referencia: aproximadamente 357 km em linha reta.
    distancia = calcular_distancia_em_metros(-23.550520, -46.633308, -22.906847, -43.172896)

    assert 355_000 < distancia < 362_000


def test_distancia_e_simetrica() -> None:
    ida = calcular_distancia_em_metros(-23.556677, -46.633088, -22.900011, -43.200022)
    volta = calcular_distancia_em_metros(-22.900011, -43.200022, -23.556677, -46.633088)

    assert ida == volta


def test_um_grau_de_latitude_equivale_a_cerca_de_111_km() -> None:
    distancia = calcular_distancia_em_metros(0.000000, 0.000000, 1.000000, 0.000000)

    assert 110_000 < distancia < 112_000