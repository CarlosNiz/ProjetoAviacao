"""Testes das regras de negocio de importacao e gerenciamento de Faixas."""
import pytest

from app.exceptions import (
    ArquivoDeImportacaoInvalidoError,
    FaixaNaoEncontradaError,
    ProjetoNaoEncontradoError,
)
from app.models.projeto import Projeto
from app.services.faixa_service import FaixaService
from app.services.projeto_service import ProjetoService

# Coordenadas com exatamente 6 casas decimais, conforme exigido pelo parser.
FAIXA_1 = "faixa1;-23.556677;-46.633088;-23.557788;-46.634199"
FAIXA_2 = "faixa2;-22.900011;-43.200022;-22.910033;-43.210044"
FAIXA_1_ALTERNATIVA = "faixa1;-10.111111;-20.222222;-30.333333;-40.444444"


def _criar_projeto(db_session) -> Projeto:
    return ProjetoService(db_session).criar(numero=1, nome="Missao Norte")


def test_importa_faixas_validas(db_session) -> None:
    projeto = _criar_projeto(db_session)
    conteudo = f"{FAIXA_1}\n{FAIXA_2}"

    faixas, rejeitadas = FaixaService(db_session).importar(projeto.id, conteudo)

    assert len(faixas) == 2
    assert rejeitadas == []


def test_rejeita_importacao_em_projeto_inexistente(db_session) -> None:
    with pytest.raises(ProjetoNaoEncontradoError):
        FaixaService(db_session).importar(999, FAIXA_1)


def test_rejeita_arquivo_vazio(db_session) -> None:
    projeto = _criar_projeto(db_session)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "")


def test_rejeita_arquivo_sem_faixas_validas(db_session) -> None:
    projeto = _criar_projeto(db_session)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "linha;invalida")


def test_rejeita_arquivo_com_coordenadas_fora_do_formato(db_session) -> None:
    projeto = _criar_projeto(db_session)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "faixa1;1.0;2.0;3.0;4.0")


def test_rejeita_reimportacao_de_faixa_com_mesmo_nome(db_session) -> None:
    projeto = _criar_projeto(db_session)
    FaixaService(db_session).importar(projeto.id, FAIXA_1)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, FAIXA_1_ALTERNATIVA)


def test_importa_parcialmente_ignorando_faixa_duplicada(db_session) -> None:
    projeto = _criar_projeto(db_session)
    FaixaService(db_session).importar(projeto.id, FAIXA_1)

    faixas, rejeitadas = FaixaService(db_session).importar(
        projeto.id, f"{FAIXA_1_ALTERNATIVA}\n{FAIXA_2}"
    )

    assert len(faixas) == 1
    assert faixas[0].nome == "faixa2"
    assert len(rejeitadas) == 1


def test_atualiza_estado_da_faixa(db_session) -> None:
    projeto = _criar_projeto(db_session)
    faixas, _ = FaixaService(db_session).importar(projeto.id, FAIXA_1)

    faixa_atualizada = FaixaService(db_session).atualizar_estado(
        projeto.id, faixas[0].id, executada=True
    )

    assert faixa_atualizada.executada is True


def test_nao_permite_alterar_faixa_de_outro_projeto(db_session) -> None:
    projeto_a = _criar_projeto(db_session)
    projeto_b = ProjetoService(db_session).criar(numero=2, nome="Missao Sul")
    faixas, _ = FaixaService(db_session).importar(projeto_a.id, FAIXA_1)

    with pytest.raises(FaixaNaoEncontradaError):
        FaixaService(db_session).atualizar_estado(projeto_b.id, faixas[0].id, executada=True)


def test_calcula_e_persiste_a_distancia_na_importacao(db_session) -> None:
    projeto = _criar_projeto(db_session)

    faixas, _ = FaixaService(db_session).importar(projeto.id, FAIXA_1)

    assert faixas[0].distancia_metros > 0