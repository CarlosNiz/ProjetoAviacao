"""Endpoints REST para importacao e gerenciamento de Faixas dentro de um Projeto."""
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ArquivoDeImportacaoInvalidoError, FalhaAoProcessarArquivoError
from app.schemas.faixa import (
    FaixaAtualizarEstado,
    FaixaResumo,
    LinhaRejeitada,
    ResultadoImportacao,
)
from app.services.faixa_service import FaixaService

router = APIRouter(prefix="/projetos/{projeto_id}/faixas", tags=["faixas"])


@router.post("/importar", response_model=ResultadoImportacao, status_code=status.HTTP_201_CREATED)
async def importar_faixas(
    projeto_id: int, arquivo: UploadFile = File(...), db: Session = Depends(get_db)
) -> ResultadoImportacao:
    nome_arquivo = arquivo.filename or ""
    if not nome_arquivo.lower().endswith(".txt"):
        raise ArquivoDeImportacaoInvalidoError(
            f"formato de arquivo invalido: '{nome_arquivo}' - esperado um arquivo .txt"
        )

    conteudo_bytes = await arquivo.read()
    try:
        conteudo = conteudo_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FalhaAoProcessarArquivoError(
            "nao foi possivel ler o arquivo: codificacao invalida, esperado UTF-8."
        ) from exc

    faixas_salvas, linhas_rejeitadas = FaixaService(db).importar(projeto_id, conteudo)

    return ResultadoImportacao(
        projeto_id=projeto_id,
        faixas_importadas=[FaixaResumo.model_validate(f) for f in faixas_salvas],
        linhas_rejeitadas=[
            LinhaRejeitada(
                numero_linha=linha.numero_linha, conteudo=linha.conteudo, motivo=linha.motivo
            )
            for linha in linhas_rejeitadas
        ],
        mensagem=(
            f"{len(faixas_salvas)} faixa(s) importada(s) com sucesso. "
            f"{len(linhas_rejeitadas)} linha(s) rejeitada(s)."
        ),
    )


@router.get("", response_model=list[FaixaResumo])
def listar_faixas(projeto_id: int, db: Session = Depends(get_db)) -> list[FaixaResumo]:
    faixas = FaixaService(db).listar_por_projeto(projeto_id)
    return [FaixaResumo.model_validate(f) for f in faixas]


@router.patch("/{faixa_id}", response_model=FaixaResumo)
def atualizar_estado_faixa(
    projeto_id: int, faixa_id: int, dados: FaixaAtualizarEstado, db: Session = Depends(get_db)
) -> FaixaResumo:
    faixa = FaixaService(db).atualizar_estado(projeto_id, faixa_id, dados.executada)
    return FaixaResumo.model_validate(faixa)


@router.delete("/{faixa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_faixa(projeto_id: int, faixa_id: int, db: Session = Depends(get_db)) -> None:
    FaixaService(db).excluir(projeto_id, faixa_id)