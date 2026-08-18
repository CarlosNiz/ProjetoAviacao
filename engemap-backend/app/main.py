"""Ponto de entrada da API REST do backend Engemap."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.exceptions import ErroDeNegocio
from app.models import Faixa, Projeto  # noqa: F401  (garante que os modelos sejam registrados)
from app.routes.faixas import router as faixas_router
from app.routes.projetos import router as projetos_router
from fastapi.exceptions import RequestValidationError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Criacao simples de tabelas via metadata, adequada ao prazo do projeto.
    # Para evolucao futura, adotar Alembic permitiria versionar o schema.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Engemap API", version="0.1.0", lifespan=lifespan)

# CORS liberado para desenvolvimento local, ja que o frontend Electron consome
# a API a partir de um processo separado.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
def tratar_erro_de_validacao(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Converte erros de validacao do Pydantic no mesmo formato dos erros de negocio."""
    problemas = [
        f"{'.'.join(str(p) for p in erro['loc'][1:])}: {erro['msg']}" for erro in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"mensagem": f"Dados invalidos - {'; '.join(problemas)}"},
    )


app.include_router(projetos_router)
app.include_router(faixas_router)


@app.get("/saude")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}