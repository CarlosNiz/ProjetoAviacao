"""
Exceções de negocio do sistema.

Cada exceção carrega uma mensagem clara, pronta para ser exibida ao usuario
(regra de negocio: toda operacao deve resultar em uma mensagem compreensivel
de sucesso ou erro), e um status_code HTTP associado.
"""


class ErroDeNegocio(Exception):
    """Exceção base para erros de regra de negocio."""

    status_code: int = 400

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class ProjetoNumeroDuplicadoError(ErroDeNegocio):
    """O numero de projeto informado ja esta em uso por outro projeto."""

    def __init__(self, numero: int) -> None:
        super().__init__(f"Ja existe um projeto cadastrado com o numero {numero}.")


class ProjetoNaoEncontradoError(ErroDeNegocio):
    """Nenhum projeto foi encontrado com o id informado."""

    status_code = 404

    def __init__(self, projeto_id: int) -> None:
        super().__init__(f"Projeto com id {projeto_id} nao foi encontrado.")


class FaixaNaoEncontradaError(ErroDeNegocio):
    """Nenhuma faixa foi encontrada com o id informado dentro do projeto."""

    status_code = 404

    def __init__(self, faixa_id: int) -> None:
        super().__init__(f"Faixa com id {faixa_id} nao foi encontrada.")


class ArquivoDeImportacaoInvalidoError(ErroDeNegocio):
    """Arquivo vazio, com extensão incorreta ou sem nenhuma faixa valida."""


class FalhaAoProcessarArquivoError(ErroDeNegocio):
    """Falha inesperada ao ler o arquivo ou ao armazenar as faixas importadas."""