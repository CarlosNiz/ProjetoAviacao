"""
Calculo de distancia entre coordenadas geograficas.

Metodo adotado: formula de haversine, que calcula a distancia great-circle
(o menor caminho sobre a superficie) entre dois pontos a partir de suas
latitudes e longitudes, assumindo a Terra como uma esfera.

A escolha considera que as faixas de voo sao segmentos relativamente curtos:
o modelo esferico introduz erro de ate cerca de 0,5% frente a um modelo
elipsoidal (WGS-84), diferenca irrelevante nesta escala e que dispensa
dependencia externa.

Unidade de medida: todas as distancias sao calculadas e armazenadas em
METROS. A conversao para quilometros e responsabilidade da camada de
apresentacao.
"""
import math

# Raio medio da Terra em metros, conforme definido pela IUGG.
RAIO_MEDIO_DA_TERRA_EM_METROS = 6_371_008.8


def calcular_distancia_em_metros(
    latitude_a: float, longitude_a: float, latitude_b: float, longitude_b: float
) -> float:
    """Distancia em metros entre dois pontos geograficos, pela formula de haversine."""
    lat_a, lon_a, lat_b, lon_b = map(
        math.radians, (latitude_a, longitude_a, latitude_b, longitude_b)
    )
    diferenca_de_latitude = lat_b - lat_a
    diferenca_de_longitude = lon_b - lon_a

    metade_do_angulo = (
        math.sin(diferenca_de_latitude / 2) ** 2
        + math.cos(lat_a) * math.cos(lat_b) * math.sin(diferenca_de_longitude / 2) ** 2
    )
    return 2 * RAIO_MEDIO_DA_TERRA_EM_METROS * math.asin(math.sqrt(metade_do_angulo))