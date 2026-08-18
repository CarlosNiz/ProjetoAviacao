"""Acesso a dados da entidade Projeto (camada de repositorio)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.projeto import Projeto


class ProjetoRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def buscar_por_numero(self, numero: int) -> Projeto | None:
        stmt = select(Projeto).where(Projeto.numero == numero)
        return self._db.scalar(stmt)

    def buscar_por_id(self, projeto_id: int) -> Projeto | None:
        return self._db.get(Projeto, projeto_id)

    def listar_todos(self) -> list[Projeto]:
        stmt = select(Projeto).order_by(Projeto.numero)
        return list(self._db.scalars(stmt))

    def salvar(self, projeto: Projeto) -> Projeto:
        self._db.add(projeto)
        self._db.commit()
        self._db.refresh(projeto)
        return projeto

    def excluir(self, projeto: Projeto) -> None:
        self._db.delete(projeto)
        self._db.commit()