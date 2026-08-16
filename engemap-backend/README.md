# Engemap Backend

API REST em FastAPI para gerenciamento de Projetos (Missões) e Faixas de
coordenadas a serem executadas por uma aeronave.

## Stack

- **Python 3.12** + **FastAPI**
- **SQLAlchemy** (ORM) + **PostgreSQL** (via Docker)
- **Pydantic** (validação e schemas da API)
- **pytest** (testes automatizados)

## Estrutura

```
app/
  main.py                     # app FastAPI, CORS, tratamento de erros
  config.py                   # configurações via variável de ambiente
  database.py                 # engine/sessão SQLAlchemy
  exceptions.py                # erros de negócio (mensagem + status HTTP)
  models/                      # ORM: Projeto, Faixa
  schemas/                     # DTOs Pydantic (contratos de entrada/saída da API)
  repositories/                # acesso a dados, sem regra de negócio
  services/                    # regras de negócio
    faixa_importer.py          # parser puro do .txt (sem I/O, fácil de testar)
    faixa_service.py
    projeto_service.py
  routes/                       # endpoints REST
tests/                          # pytest, banco SQLite em memória
```

A separação segue o fluxo `routes` → `services` (regra de negócio) →
`repositories` (acesso a dados) → `models`.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (para o PostgreSQL)

## Como rodar

1. Suba o banco de dados (a partir da raiz do monorepo, onde está o
   `docker-compose.yml`):
   ```bash
   docker compose up -d
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   cd engemap-backend
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Copie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   Os valores padrão já batem com as credenciais do `docker-compose.yml`
   (usuário/senha/banco `engemap`), não precisa editar nada para rodar local.

5. Suba a API:
   ```bash
   python3 -m uvicorn app.main:app --reload
   ```
   Documentação interativa (Swagger) em `http://localhost:8000/docs`.

   > Se o comando `uvicorn` sozinho não for encontrado, use sempre
   > `python3 -m uvicorn ...` — isso garante que o Python da venv ativa seja
   > usado, evitando conflito com outras instalações do sistema (ex: `asdf`).

As tabelas são criadas automaticamente no startup (`Base.metadata.create_all`),
não é necessário rodar migração manualmente.

## Rodar os testes

```bash
python3 -m pytest -v
```

Os testes usam **SQLite em memória**, não o PostgreSQL do Docker não é
necessário o banco estar rodando para testar. Isso é intencional (princípio
F.I.R.S.T: testes rápidos e independentes de infraestrutura externa); nenhuma
regra de negócio testada depende de recurso específico do PostgreSQL.

## Endpoints

| Método | Rota                                        | Descrição                           |
|--------|---------------------------------------------|-------------------------------------|
| POST   | `/projetos`                                 | Cadastrar projeto                   |
| GET    | `/projetos`                                 | Listar projetos                     |
| GET    | `/projetos/{id}`                            | Detalhe do projeto + faixas         |
| DELETE | `/projetos/{id}`                            | Excluir projeto (e suas faixas)     |
| POST   | `/projetos/{id}/faixas/importar`            | Importar faixas via arquivo `.txt`  |
| GET    | `/projetos/{id}/faixas`                     | Listar faixas do projeto            |
| PATCH  | `/projetos/{id}/faixas/{faixa_id}`          | Atualizar estado (executada)        |
| DELETE | `/projetos/{id}/faixas/{faixa_id}`          | Excluir faixa                       |

Erros de regra de negócio sempre respondem no formato `{"mensagem": "..."}`,
pronto para exibição direta na interface do frontend.

## Formato do arquivo de importação de faixas

Arquivo `.txt`, uma faixa por linha, campos separados por `;`:

```
nome;latitude_a;longitude_a;latitude_b;longitude_b
```

Exemplo:

```
faixa1;-23.55;-46.63;-23.56;-46.64
faixa2;-22.90;-43.20;-22.91;-43.21
```