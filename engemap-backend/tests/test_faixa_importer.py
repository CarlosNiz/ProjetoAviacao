"""Testes do parser de arquivos de faixas (regra mais sensivel a erro do sistema)."""
from app.services.faixa_importer import parsear_conteudo


def test_parseia_linhas_validas() -> None:
    conteudo = "faixa1;1.0;2.0;3.0;4.0\nfaixa2;5.5;6.5;7.5;8.5"

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 2
    assert resultado.linhas_rejeitadas == []
    assert resultado.faixas[0].nome == "faixa1"
    assert resultado.faixas[0].latitude_a == 1.0


def test_rejeita_linha_com_numero_errado_de_campos() -> None:
    conteudo = "faixa1;1.0;2.0;3.0"  # faltando um campo

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert len(resultado.linhas_rejeitadas) == 1
    assert resultado.linhas_rejeitadas[0].numero_linha == 1


def test_rejeita_linha_com_coordenada_nao_numerica() -> None:
    conteudo = "faixa1;abc;2.0;3.0;4.0"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert "numeros validos" in resultado.linhas_rejeitadas[0].motivo


def test_ignora_linhas_em_branco() -> None:
    conteudo = "faixa1;1.0;2.0;3.0;4.0\n\n   \nfaixa2;5.0;6.0;7.0;8.0"

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 2
    assert resultado.linhas_rejeitadas == []


def test_rejeita_nome_duplicado_dentro_do_proprio_arquivo() -> None:
    conteudo = "faixa1;1.0;2.0;3.0;4.0\nfaixa1;9.0;9.0;9.0;9.0"

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 1
    assert len(resultado.linhas_rejeitadas) == 1
    assert "duplicado" in resultado.linhas_rejeitadas[0].motivo