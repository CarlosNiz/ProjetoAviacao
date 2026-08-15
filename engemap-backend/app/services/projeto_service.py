"""Regras de negocio relacionadas a Projeto."""
from sqlalchemy.orm import Session

from app.exceptions import ProjetoNaoEncontradoError, ProjetoNumeroDuplicadoError
from app.models.projeto import Projeto
from app.repositories.projeto_repository import ProjetoRepository


class ProjetoService:
    def __init__(self, db: Session) -> None:
        self._repo = ProjetoRepository(db)

    def criar(self, numero: str, nome: str) -> Projeto:
        """Cadastra um projeto. O numero e o identificador de negocio e deve ser unico."""
        if self._repo.buscar_por_numero(numero) is not None:
            raise ProjetoNumeroDuplicadoError(numero)
        return self._repo.salvar(Projeto(numero=numero, nome=nome))

    def listar_todos(self) -> list[Projeto]:
        return self._repo.listar_todos()

    def buscar_por_id(self, projeto_id: int) -> Projeto:
        projeto = self._repo.buscar_por_id(projeto_id)
        if projeto is None:
            raise ProjetoNaoEncontradoError(projeto_id)
        return projeto

    def excluir(self, projeto_id: int) -> None:
        projeto = self.buscar_por_id(projeto_id)
        self._repo.excluir(projeto)