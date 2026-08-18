"""Testes das regras de negocio de Projeto."""
import pytest
from pydantic import ValidationError

from app.exceptions import ProjetoNaoEncontradoError, ProjetoNumeroDuplicadoError
from app.schemas.projeto import ProjetoCriar
from app.services.projeto_service import ProjetoService


def test_cria_projeto_com_sucesso(db_session) -> None:
    servico = ProjetoService(db_session)

    projeto = servico.criar(numero=1, nome="Missao Norte")

    assert projeto.id is not None
    assert projeto.numero == 1


def test_rejeita_numero_de_projeto_duplicado(db_session) -> None:
    servico = ProjetoService(db_session)
    servico.criar(numero=1, nome="Missao Norte")

    with pytest.raises(ProjetoNumeroDuplicadoError):
        servico.criar(numero=1, nome="Outra Missao")


def test_lanca_erro_ao_buscar_projeto_inexistente(db_session) -> None:
    servico = ProjetoService(db_session)

    with pytest.raises(ProjetoNaoEncontradoError):
        servico.buscar_por_id(999)


def test_rejeita_numero_de_projeto_nao_inteiro() -> None:
    with pytest.raises(ValidationError):
        ProjetoCriar(numero="P001", nome="Missao Norte")


def test_rejeita_numero_de_projeto_zero_ou_negativo() -> None:
    with pytest.raises(ValidationError):
        ProjetoCriar(numero=0, nome="Missao Norte")

    with pytest.raises(ValidationError):
        ProjetoCriar(numero=-5, nome="Missao Norte")


def test_rejeita_nome_de_projeto_acima_de_64_caracteres() -> None:
    with pytest.raises(ValidationError):
        ProjetoCriar(numero=1, nome="x" * 65)