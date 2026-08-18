"""
Responsavel por interpretar o conteudo de um arquivo .txt de faixas.

Cada linha valida deve seguir o formato:
    nome;latitude_a;longitude_a;latitude_b;longitude_b

As coordenadas devem ter exatamente 6 casas decimais. A verificacao e feita
sobre o texto original, antes da conversao para float, porque a conversao
descarta zeros a direita (float("1.500000") == 1.5) e tornaria impossivel
distinguir "1.5" de "1.500000".

Decisao de projeto: linhas mal formatadas ou com nomes duplicados sao
reportadas individualmente e NAO interrompem o processamento das demais
linhas do arquivo (importacao parcial). A camada de servico decide se a
importacao como um todo deve falhar (por exemplo, quando nenhuma faixa
valida sobrar). Esta funcao e pura (sem I/O), o que a torna facil e rapida
de testar isoladamente.
"""
import re
from dataclasses import dataclass

CAMPOS_ESPERADOS = 5
CASAS_DECIMAIS_EXIGIDAS = 6

# Aceita sinal opcional, parte inteira e exatamente 6 casas decimais.
# Notacao cientifica e rejeitada de proposito: o formato de entrada e fixo.
PADRAO_COORDENADA = re.compile(r"^[+-]?\d+\.\d{6}$")

ROTULOS_DAS_COORDENADAS = ("latitude A", "longitude A", "latitude B", "longitude B")


@dataclass
class FaixaImportada:
    nome: str
    latitude_a: float
    longitude_a: float
    latitude_b: float
    longitude_b: float


@dataclass
class LinhaRejeitada:
    numero_linha: int
    conteudo: str
    motivo: str


@dataclass
class ResultadoParsing:
    faixas: list[FaixaImportada]
    linhas_rejeitadas: list[LinhaRejeitada]


def parsear_conteudo(conteudo: str) -> ResultadoParsing:
    """Converte o conteudo bruto do arquivo em faixas validas e linhas rejeitadas."""
    faixas: list[FaixaImportada] = []
    linhas_rejeitadas: list[LinhaRejeitada] = []
    nomes_ja_vistos: set[str] = set()

    for numero_linha, linha_bruta in enumerate(conteudo.splitlines(), start=1):
        linha = linha_bruta.strip()
        if not linha:
            continue

        resultado_linha = _parsear_linha(linha, numero_linha)
        if isinstance(resultado_linha, LinhaRejeitada):
            linhas_rejeitadas.append(resultado_linha)
            continue

        if resultado_linha.nome in nomes_ja_vistos:
            linhas_rejeitadas.append(
                LinhaRejeitada(
                    numero_linha=numero_linha,
                    conteudo=linha,
                    motivo=f"nome de faixa '{resultado_linha.nome}' duplicado no proprio arquivo.",
                )
            )
            continue

        nomes_ja_vistos.add(resultado_linha.nome)
        faixas.append(resultado_linha)

    return ResultadoParsing(faixas=faixas, linhas_rejeitadas=linhas_rejeitadas)


def _parsear_linha(linha: str, numero_linha: int) -> FaixaImportada | LinhaRejeitada:
    """Interpreta uma unica linha no formato string;double;double;double;double."""
    campos = linha.split(";")
    if len(campos) != CAMPOS_ESPERADOS:
        return LinhaRejeitada(
            numero_linha=numero_linha,
            conteudo=linha,
            motivo=(
                f"esperado {CAMPOS_ESPERADOS} campos separados por ';', "
                f"encontrado {len(campos)}."
            ),
        )

    nome = campos[0].strip()
    if not nome:
        return LinhaRejeitada(
            numero_linha=numero_linha, conteudo=linha, motivo="nome da faixa nao pode ser vazio."
        )

    coordenadas: list[float] = []
    for rotulo, texto_bruto in zip(ROTULOS_DAS_COORDENADAS, campos[1:], strict=True):
        texto = texto_bruto.strip()
        if not PADRAO_COORDENADA.match(texto):
            return LinhaRejeitada(
                numero_linha=numero_linha,
                conteudo=linha,
                motivo=(
                    f"{rotulo} invalida: '{texto}' - esperado um numero com exatamente "
                    f"{CASAS_DECIMAIS_EXIGIDAS} casas decimais (ex: -23.556677)."
                ),
            )
        coordenadas.append(float(texto))

    return FaixaImportada(
        nome=nome,
        latitude_a=coordenadas[0],
        longitude_a=coordenadas[1],
        latitude_b=coordenadas[2],
        longitude_b=coordenadas[3],
    )