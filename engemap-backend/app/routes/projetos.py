"""Endpoints REST para gerenciamento de Projetos."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.projeto import ProjetoCriar, ProjetoDetalhe, ProjetoResumo
from app.services.projeto_service import ProjetoService

router = APIRouter(prefix="/projetos", tags=["projetos"])


@router.post("", response_model=ProjetoResumo, status_code=status.HTTP_201_CREATED)
def criar_projeto(dados: ProjetoCriar, db: Session = Depends(get_db)) -> ProjetoResumo:
    projeto = ProjetoService(db).criar(numero=dados.numero, nome=dados.nome)
    return ProjetoResumo.model_validate(projeto)


@router.get("", response_model=list[ProjetoResumo])
def listar_projetos(db: Session = Depends(get_db)) -> list[ProjetoResumo]:
    projetos = ProjetoService(db).listar_todos()
    return [ProjetoResumo.model_validate(projeto) for projeto in projetos]


@router.get("/{projeto_id}", response_model=ProjetoDetalhe)
def obter_projeto(projeto_id: int, db: Session = Depends(get_db)) -> ProjetoDetalhe:
    projeto = ProjetoService(db).buscar_por_id(projeto_id)
    return ProjetoDetalhe.model_validate(projeto)


@router.delete("/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_projeto(projeto_id: int, db: Session = Depends(get_db)) -> None:
    ProjetoService(db).excluir(projeto_id)