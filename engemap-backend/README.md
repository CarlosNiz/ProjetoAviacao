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
  main.py                      # app FastAPI, CORS, tratamento de erros
  config.py                    # configurações via variável de ambiente
  database.py                  # engine/sessão SQLAlchemy
  exceptions.py                # erros de negócio (mensagem + status HTTP)
  models/                      # ORM: Projeto, Faixa
  schemas/                     # DTOs Pydantic (contratos de entrada/saída da API)
  repositories/                # acesso a dados, sem regra de negócio
  services/                    # regras de negócio
    faixa_importer.py          # parser puro do .txt (sem I/O, fácil de testar)
    faixa_service.py
    geodesia.py                # cálculo de distância (haversine)
    projeto_service.py
    resumo_de_execucao.py      # distâncias somadas e percentual de execução
  routes/                      # endpoints REST
tests/                         # pytest, banco SQLite em memória
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
   > `python3 -m uvicorn ...`, o que garante que o Python da venv ativa seja
   > usado, evitando conflito com outras instalações do sistema (ex: `asdf`).

As tabelas são criadas automaticamente no startup (`Base.metadata.create_all`),
não é necessário rodar migração manualmente.

> ⚠️ O `create_all` apenas **cria** tabelas inexistentes, nunca altera as
> existentes. Ao mudar um modelo durante o desenvolvimento (tipo de coluna,
> tamanho, coluna nova), é necessário recriar as tabelas:
> ```bash
> docker compose exec db psql -U engemap -d engemap -c "DROP TABLE faixas, projetos CASCADE;"
> ```
> Isso apaga os dados existentes. Em produção, o caminho adequado seria
> adotar Alembic para versionar o schema com migrações.

## Rodar os testes

```bash
python3 -m pytest -v
```

Os testes usam **SQLite em memória**, não o PostgreSQL do Docker, então não é
necessário o banco estar rodando para testar. Isso é intencional (princípio
F.I.R.S.T: testes rápidos e independentes de infraestrutura externa); nenhuma
regra de negócio testada depende de recurso específico do PostgreSQL.

A cobertura prioriza as regras mais sensíveis a erro: parsing do arquivo de
faixas, validação de duplicidade de projeto e de faixa, cálculo de distância
e cálculo do percentual de execução.

## Endpoints

| Método | Rota                                        | Descrição                            |
|--------|---------------------------------------------|--------------------------------------|
| POST   | `/projetos`                                 | Cadastrar projeto                    |
| GET    | `/projetos`                                 | Listar projetos                      |
| GET    | `/projetos/{id}`                            | Detalhe do projeto, faixas e resumo  |
| DELETE | `/projetos/{id}`                            | Excluir projeto (e suas faixas)      |
| POST   | `/projetos/{id}/faixas/importar`            | Importar faixas via arquivo `.txt`   |
| GET    | `/projetos/{id}/faixas`                     | Listar faixas do projeto             |
| PATCH  | `/projetos/{id}/faixas/{faixa_id}`          | Atualizar estado (executada)         |
| DELETE | `/projetos/{id}/faixas/{faixa_id}`          | Excluir faixa                        |

Erros de regra de negócio sempre respondem no formato `{"mensagem": "..."}`,
pronto para exibição direta na interface do frontend.

## Formato do arquivo de importação de faixas

Arquivo `.txt`, uma faixa por linha, campos separados por `;`. As coordenadas
devem ter **exatamente 6 casas decimais**:

```
nome;latitude_a;longitude_a;latitude_b;longitude_b
```

Exemplo:

```
faixa1;-23.556677;-46.633088;-23.557788;-46.634199
faixa2;-22.900011;-43.200022;-22.910033;-43.210044
```

O arquivo funciona apenas como meio de entrada: nenhuma cópia dele é mantida
pelo sistema, apenas as faixas nele contidas são persistidas.

## Regras de validação

**Projeto**

- `numero`: inteiro positivo, único no sistema (identificador de negócio)
- `nome`: obrigatório, até 64 caracteres

**Faixa**

- nome único dentro do projeto
- coordenadas com exatamente 6 casas decimais
- linhas inválidas são rejeitadas individualmente e reportadas com o número da
  linha e o motivo; a importação só falha por completo se nenhuma faixa válida
  restar ao final

A verificação das casas decimais é feita sobre o texto original, antes da
conversão para `float`, porque a conversão descarta zeros à direita
(`float("1.500000") == 1.5`) e tornaria impossível distinguir `1.5` de
`1.500000`.

Erros de validação do Pydantic são convertidos para o mesmo formato dos erros
de negócio (`{"mensagem": "..."}`), mantendo o contrato consistente para o
frontend.

## Cálculo de distância

A distância de cada faixa é calculada entre os pontos A e B pela **fórmula de
haversine**, que determina a distância *great-circle* (o menor caminho sobre a
superfície) a partir das latitudes e longitudes, assumindo a Terra como uma
esfera de raio médio 6.371.008,8 m (valor definido pela IUGG).

**Unidade adotada: metros.** O valor é persistido na coluna
`faixas.distancia_metros` no momento da importação. Como as coordenadas não são
editáveis após a importação, não há risco do valor ficar defasado. A conversão
para quilômetros ocorre apenas na camada de apresentação.

A escolha pelo modelo esférico considera que as faixas de voo são segmentos
curtos: o erro frente a um modelo elipsoidal (WGS-84, via fórmula de Vincenty)
é de até cerca de 0,5%, irrelevante nesta escala, e dispensa dependência
externa.

## Percentual de execução

O progresso do projeto é derivado das distâncias calculadas:

```
percentual_executado = (soma das distâncias das faixas executadas /
                        soma das distâncias de todas as faixas) × 100
```

O endpoint de detalhe do projeto (`GET /projetos/{id}`) retorna, além das
faixas, um objeto `resumo` contendo:

- `distancia_total_metros`: soma das distâncias de todas as faixas
- `distancia_executada_metros`: soma das distâncias das faixas executadas
- `percentual_executado`: percentual conforme a fórmula acima
- `faixas_executadas` e `total_de_faixas`: contagens para exibição

Projetos sem faixas retornam 0%, evitando divisão por zero.