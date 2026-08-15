"""
Responsável por interpretar o conteudo de um arquivo .txt de faixas.

Cada linha valida deve seguir o formato:
    nome;latitude_a;longitude_a;latitude_b;longitude_b

Decisão de projeto: linhas mal formatadas ou com nomes duplicados são
reportadas individualmente e NÃO interrompem o processamento das demais
linhas do arquivo (importacao parcial). A camada de servico decide se a
importa~ão como um todo deve falhar (por exemplo, quando nenhuma faixa
valida sobrar). Esta função e pura (sem I/O), o que a torna fácil e rápida
de testar isoladamente.
"""
from dataclasses import dataclass

CAMPOS_ESPERADOS = 5


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

    try:
        latitude_a = float(campos[1].strip())
        longitude_a = float(campos[2].strip())
        latitude_b = float(campos[3].strip())
        longitude_b = float(campos[4].strip())
    except ValueError:
        return LinhaRejeitada(
            numero_linha=numero_linha,
            conteudo=linha,
            motivo="latitude e longitude precisam ser numeros validos (double).",
        )

    return FaixaImportada(
        nome=nome,
        latitude_a=latitude_a,
        longitude_a=longitude_a,
        latitude_b=latitude_b,
        longitude_b=longitude_b,
    )