"""Testes das regras de negocio de Projeto."""
import pytest

from app.exceptions import ProjetoNaoEncontradoError, ProjetoNumeroDuplicadoError
from app.services.projeto_service import ProjetoService


def test_cria_projeto_com_sucesso(db_session) -> None:
    servico = ProjetoService(db_session)

    projeto = servico.criar(numero="P001", nome="Missao Norte")

    assert projeto.id is not None
    assert projeto.numero == "P001"


def test_rejeita_numero_de_projeto_duplicado(db_session) -> None:
    servico = ProjetoService(db_session)
    servico.criar(numero="P001", nome="Missao Norte")

    with pytest.raises(ProjetoNumeroDuplicadoError):
        servico.criar(numero="P001", nome="Outra Missao")


def test_lanca_erro_ao_buscar_projeto_inexistente(db_session) -> None:
    servico = ProjetoService(db_session)

    with pytest.raises(ProjetoNaoEncontradoError):
        servico.buscar_por_id(999)