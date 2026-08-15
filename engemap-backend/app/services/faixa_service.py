"""Regras de negocio relacionadas a Faixa: importacao, alteracao de estado e exclusao."""
from sqlalchemy.orm import Session

from app.exceptions import (
    ArquivoDeImportacaoInvalidoError,
    FaixaNaoEncontradaError,
    ProjetoNaoEncontradoError,
)
from app.models.faixa import Faixa
from app.repositories.faixa_repository import FaixaRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.services.faixa_importer import LinhaRejeitada, parsear_conteudo


class FaixaService:
    def __init__(self, db: Session) -> None:
        self._faixa_repo = FaixaRepository(db)
        self._projeto_repo = ProjetoRepository(db)

    def importar(
        self, projeto_id: int, conteudo: str
    ) -> tuple[list[Faixa], list[LinhaRejeitada]]:
        """
        Importa faixas de um arquivo .txt dentro de um projeto ja cadastrado.

        Linhas invalidas ou com nomes ja usados no projeto sao rejeitadas
        individualmente e reportadas ao usuario; a operacao so falha por
        completo se nenhuma faixa valida restar ao final (arquivo vazio ou
        sem nenhuma faixa valida e tratado como erro).
        """
        projeto = self._projeto_repo.buscar_por_id(projeto_id)
        if projeto is None:
            raise ProjetoNaoEncontradoError(projeto_id)

        if not conteudo.strip():
            raise ArquivoDeImportacaoInvalidoError("O arquivo enviado esta vazio.")

        resultado = parsear_conteudo(conteudo)
        linhas_rejeitadas = list(resultado.linhas_rejeitadas)

        novas_faixas: list[Faixa] = []
        for faixa_importada in resultado.faixas:
            if self._faixa_repo.existe_com_nome(projeto_id, faixa_importada.nome):
                linhas_rejeitadas.append(
                    LinhaRejeitada(
                        numero_linha=0,
                        conteudo=faixa_importada.nome,
                        motivo=(
                            f"ja existe uma faixa chamada '{faixa_importada.nome}' "
                            "neste projeto."
                        ),
                    )
                )
                continue
            novas_faixas.append(
                Faixa(
                    projeto_id=projeto_id,
                    nome=faixa_importada.nome,
                    latitude_a=faixa_importada.latitude_a,
                    longitude_a=faixa_importada.longitude_a,
                    latitude_b=faixa_importada.latitude_b,
                    longitude_b=faixa_importada.longitude_b,
                )
            )

        if not novas_faixas:
            raise ArquivoDeImportacaoInvalidoError(
                "Nenhuma faixa valida foi encontrada no arquivo enviado."
            )

        faixas_salvas = self._faixa_repo.salvar_muitas(novas_faixas)
        return faixas_salvas, linhas_rejeitadas

    def listar_por_projeto(self, projeto_id: int) -> list[Faixa]:
        if self._projeto_repo.buscar_por_id(projeto_id) is None:
            raise ProjetoNaoEncontradoError(projeto_id)
        return self._faixa_repo.listar_por_projeto(projeto_id)

    def atualizar_estado(self, projeto_id: int, faixa_id: int, executada: bool) -> Faixa:
        faixa = self._buscar_faixa_do_projeto(projeto_id, faixa_id)
        return self._faixa_repo.atualizar_estado(faixa, executada)

    def excluir(self, projeto_id: int, faixa_id: int) -> None:
        faixa = self._buscar_faixa_do_projeto(projeto_id, faixa_id)
        self._faixa_repo.excluir(faixa)

    def _buscar_faixa_do_projeto(self, projeto_id: int, faixa_id: int) -> Faixa:
        """Garante que a faixa pertence ao projeto informado na URL."""
        faixa = self._faixa_repo.buscar_por_id(faixa_id)
        if faixa is None or faixa.projeto_id != projeto_id:
            raise FaixaNaoEncontradaError(faixa_id)
        return faixa