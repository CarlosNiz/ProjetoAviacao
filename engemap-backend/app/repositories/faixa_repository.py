"""Acesso a dados da entidade Faixa (camada de repositorio)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.faixa import Faixa


class FaixaRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def existe_com_nome(self, projeto_id: int, nome: str) -> bool:
        stmt = select(Faixa.id).where(Faixa.projeto_id == projeto_id, Faixa.nome == nome)
        return self._db.scalar(stmt) is not None

    def buscar_por_id(self, faixa_id: int) -> Faixa | None:
        return self._db.get(Faixa, faixa_id)

    def listar_por_projeto(self, projeto_id: int) -> list[Faixa]:
        stmt = select(Faixa).where(Faixa.projeto_id == projeto_id).order_by(Faixa.nome)
        return list(self._db.scalars(stmt))

    def salvar_muitas(self, faixas: list[Faixa]) -> list[Faixa]:
        self._db.add_all(faixas)
        self._db.commit()
        for faixa in faixas:
            self._db.refresh(faixa)
        return faixas

    def excluir(self, faixa: Faixa) -> None:
        self._db.delete(faixa)
        self._db.commit()

    def atualizar_estado(self, faixa: Faixa, executada: bool) -> Faixa:
        faixa.executada = executada
        self._db.commit()
        self._db.refresh(faixa)
        return faixa