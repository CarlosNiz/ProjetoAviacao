"""Testes do parser de arquivos de faixas (regra mais sensivel a erro do sistema)."""
from app.services.faixa_importer import parsear_conteudo


def test_parseia_linhas_validas() -> None:
    conteudo = (
        "faixa1;-23.556677;-46.633088;-23.557788;-46.634199\n"
        "faixa2;-22.900011;-43.200022;-22.910033;-43.210044"
    )

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 2
    assert resultado.linhas_rejeitadas == []
    assert resultado.faixas[0].nome == "faixa1"
    assert resultado.faixas[0].latitude_a == -23.556677


def test_rejeita_linha_com_numero_errado_de_campos() -> None:
    conteudo = "faixa1;-23.556677;-46.633088;-23.557788"  # faltando um campo

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert len(resultado.linhas_rejeitadas) == 1
    assert resultado.linhas_rejeitadas[0].numero_linha == 1


def test_rejeita_linha_com_coordenada_nao_numerica() -> None:
    conteudo = "faixa1;abc;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert "latitude A invalida" in resultado.linhas_rejeitadas[0].motivo


def test_rejeita_coordenada_com_menos_de_seis_casas_decimais() -> None:
    conteudo = "faixa1;-23.5566;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert "6 casas decimais" in resultado.linhas_rejeitadas[0].motivo


def test_rejeita_coordenada_com_mais_de_seis_casas_decimais() -> None:
    conteudo = "faixa1;-23.5566778;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert "latitude A invalida" in resultado.linhas_rejeitadas[0].motivo


def test_rejeita_coordenada_sem_casas_decimais() -> None:
    conteudo = "faixa1;-23;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []


def test_aceita_zeros_a_direita_nas_casas_decimais() -> None:
    conteudo = "faixa1;10.500000;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 1
    assert resultado.faixas[0].latitude_a == 10.5


def test_identifica_qual_coordenada_esta_invalida() -> None:
    conteudo = "faixa1;-23.556677;-46.633088;-23.55;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert "latitude B invalida" in resultado.linhas_rejeitadas[0].motivo


def test_ignora_linhas_em_branco() -> None:
    conteudo = (
        "faixa1;-23.556677;-46.633088;-23.557788;-46.634199\n"
        "\n   \n"
        "faixa2;-22.900011;-43.200022;-22.910033;-43.210044"
    )

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 2
    assert resultado.linhas_rejeitadas == []


def test_rejeita_nome_duplicado_dentro_do_proprio_arquivo() -> None:
    conteudo = (
        "faixa1;-23.556677;-46.633088;-23.557788;-46.634199\n"
        "faixa1;-22.900011;-43.200022;-22.910033;-43.210044"
    )

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 1
    assert len(resultado.linhas_rejeitadas) == 1
    assert "duplicado" in resultado.linhas_rejeitadas[0].motivo


def test_rejeita_nome_de_faixa_acima_de_64_caracteres() -> None:
    nome_longo = "x" * 65
    conteudo = f"{nome_longo};-23.556677;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert resultado.faixas == []
    assert "64 caracteres" in resultado.linhas_rejeitadas[0].motivo


def test_aceita_nome_de_faixa_com_exatamente_64_caracteres() -> None:
    nome_no_limite = "x" * 64
    conteudo = f"{nome_no_limite};-23.556677;-46.633088;-23.557788;-46.634199"

    resultado = parsear_conteudo(conteudo)

    assert len(resultado.faixas) == 1