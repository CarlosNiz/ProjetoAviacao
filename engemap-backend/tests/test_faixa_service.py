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


def _criar_projeto(db_session) -> Projeto:
    return ProjetoService(db_session).criar(numero="P001", nome="Missao Norte")


def test_importa_faixas_validas(db_session) -> None:
    projeto = _criar_projeto(db_session)
    conteudo = "faixa1;1.0;2.0;3.0;4.0\nfaixa2;5.0;6.0;7.0;8.0"

    faixas, rejeitadas = FaixaService(db_session).importar(projeto.id, conteudo)

    assert len(faixas) == 2
    assert rejeitadas == []


def test_rejeita_importacao_em_projeto_inexistente(db_session) -> None:
    with pytest.raises(ProjetoNaoEncontradoError):
        FaixaService(db_session).importar(999, "faixa1;1.0;2.0;3.0;4.0")


def test_rejeita_arquivo_vazio(db_session) -> None:
    projeto = _criar_projeto(db_session)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "")


def test_rejeita_arquivo_sem_faixas_validas(db_session) -> None:
    projeto = _criar_projeto(db_session)

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "linha;invalida")


def test_rejeita_reimportacao_de_faixa_com_mesmo_nome(db_session) -> None:
    projeto = _criar_projeto(db_session)
    FaixaService(db_session).importar(projeto.id, "faixa1;1.0;2.0;3.0;4.0")

    with pytest.raises(ArquivoDeImportacaoInvalidoError):
        FaixaService(db_session).importar(projeto.id, "faixa1;9.0;9.0;9.0;9.0")


def test_importa_parcialmente_ignorando_faixa_duplicada(db_session) -> None:
    projeto = _criar_projeto(db_session)
    FaixaService(db_session).importar(projeto.id, "faixa1;1.0;2.0;3.0;4.0")

    faixas, rejeitadas = FaixaService(db_session).importar(
        projeto.id, "faixa1;9.0;9.0;9.0;9.0\nfaixa2;1.0;1.0;1.0;1.0"
    )

    assert len(faixas) == 1
    assert faixas[0].nome == "faixa2"
    assert len(rejeitadas) == 1


def test_atualiza_estado_da_faixa(db_session) -> None:
    projeto = _criar_projeto(db_session)
    faixas, _ = FaixaService(db_session).importar(projeto.id, "faixa1;1.0;2.0;3.0;4.0")

    faixa_atualizada = FaixaService(db_session).atualizar_estado(
        projeto.id, faixas[0].id, executada=True
    )

    assert faixa_atualizada.executada is True


def test_nao_permite_alterar_faixa_de_outro_projeto(db_session) -> None:
    projeto_a = _criar_projeto(db_session)
    projeto_b = ProjetoService(db_session).criar(numero="P002", nome="Missao Sul")
    faixas, _ = FaixaService(db_session).importar(projeto_a.id, "faixa1;1.0;2.0;3.0;4.0")

    with pytest.raises(FaixaNaoEncontradaError):
        FaixaService(db_session).atualizar_estado(projeto_b.id, faixas[0].id, executada=True)