# Projeto Engemap

Teste prático — aplicação desktop para gerenciamento de **Missões** (Projetos)
e suas **Faixas** de coordenadas a serem executadas por uma aeronave.

## Estrutura do repositório

```
ProjetoEngemap/
├── docker-compose.yml      # PostgreSQL para desenvolvimento
├── engemap-backend/        # API REST (Python + FastAPI)
├── engemap-frontend/       # Aplicação desktop (Electron + React + Vite)
└── readme.md
```

## Arquitetura

A aplicação é dividida em dois processos independentes que se comunicam via
**HTTP local**:

```
┌──────────────────────────┐        ┌───────────────────────────┐
│  Electron + React        │  HTTP  │  FastAPI (Python)         │
│  (engemap-frontend)      │ ─────► │  (engemap-backend)        │
│  localhost:5173 (dev)    │        │  localhost:8000           │
└──────────────────────────┘        └─────────────┬─────────────┘
                                                  │
                                                  ▼
                                    ┌───────────────────────────┐
                                    │  PostgreSQL (Docker)      │
                                    │  localhost:5432           │
                                    └───────────────────────────┘
```

A escolha por uma API REST local reduz o acoplamento entre frontend e backend e permite testar o
CRUD de projetos e a importação de faixas isoladamente, antes de integrar com
a interface.

## Stack

| Camada    | Tecnologia                              |
|-----------|-----------------------------------------|
| Frontend  | Electron, React, Vite                   |
| Backend   | Python, FastAPI, SQLAlchemy, Pydantic   |
| Banco     | PostgreSQL (via Docker)                 |
| Testes    | pytest                                  |

## Pré-requisitos

- Python 3.12+
- Node.js 18+
- Docker e Docker Compose

## Como rodar o projeto

São três terminais: banco, backend e frontend.

### 1. Banco de dados

Na raiz do repositório:

```bash
docker compose up -d
```

Verifique se subiu:

```bash
docker compose ps
```

### 2. Backend

```bash
cd engemap-backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 -m uvicorn app.main:app --reload
```

API disponível em `http://localhost:8000`
Documentação interativa (Swagger) em `http://localhost:8000/docs`.

Detalhes em [`engemap-backend/README.md`](engemap-backend/README.md).

### 3. Frontend

```bash
cd engemap-frontend
npm install
npm run dev
```

A janela do Electron abre automaticamente.

Detalhes em [`engemap-frontend/README.md`](engemap-frontend/README.md).

## Rodar os testes

```bash
cd engemap-backend
source .venv/bin/activate
python3 -m pytest -v
```

Os testes usam SQLite em memória, não é necessário o Docker estar rodando.

## Funcionalidades

- Cadastro de projetos com número único como identificador de negócio
- Importação de faixas a partir de arquivo `.txt`, dentro de um projeto
  previamente selecionado
- Validação de formato e de duplicidade de nome de faixa dentro do projeto
- Alteração do estado de execução da faixa (Executada / Não Executada)
- Exclusão de projetos (em cascata com suas faixas) e de faixas individuais
- Feedback claro de sucesso ou erro em toda operação

## Formato do arquivo de importação

Arquivo `.txt`, uma faixa por linha, campos separados por `;`:

```
nome;latitude_a;longitude_a;latitude_b;longitude_b
```

Exemplo:

```
faixa1;-23.55;-46.63;-23.56;-46.64
faixa2;-22.90;-43.20;-22.91;-43.21
```

O arquivo funciona apenas como meio de entrada: nenhuma cópia dele é mantida
pelo sistema, apenas as faixas nele contidas são persistidas.