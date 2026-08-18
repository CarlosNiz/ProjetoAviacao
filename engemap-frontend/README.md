# Engemap Frontend

Aplicação desktop em **Electron + React (Vite)** para gerenciamento de
Missões (Projetos) e suas Faixas de coordenadas.

Consome a API REST local do [`engemap-backend`](../engemap-backend).

## Stack

- **Electron** — empacota a aplicação como app desktop
- **React** + **Vite** — interface e build com hot reload
- **vite-plugin-electron** — integra o build do Electron ao ciclo do Vite

## Estrutura

```
electron/
  main.js               # processo principal: cria a janela do app
  preload.js            # ponte controlada entre o Electron e o React
src/
  api/
    cliente.js          # cliente HTTP: URL base e tratamento de erro
    projetos.js         # chamadas de Projeto
    faixas.js           # chamadas de Faixa
  components/
    FormularioNovoProjeto.jsx
    ImportadorDeFaixas.jsx
    ListaDeProjetos.jsx
    Mensagem.jsx         # feedback de sucesso/erro
    PainelDoProjeto.jsx
    ResumoDeExecucao.jsx # distâncias e barra de progresso do projeto
    TabelaDeFaixas.jsx   # tabela ordenável, com distância por faixa
  hooks/
    useMensagem.js      # centraliza o estado de feedback ao usuário
  theme/
    cores.js            # paleta do tema escuro
  utils/
    formatarDistancia.js # converte metros para exibição (m / km)
  App.jsx               # composição da tela e orquestração das chamadas
  main.jsx              # ponto de entrada do React
```

## Interface

Tela única com dois painéis:

- **Esquerda** — cadastro e listagem de projetos, com seleção e exclusão.
- **Direita** — detalhe do projeto selecionado: resumo de execução,
  importação de faixas e tabela de faixas.

A tabela de faixas permite ordenar por nome (clique no cabeçalho) e alternar
o estado de execução de cada faixa diretamente, sem sair da tela.

## Resumo de execução

O painel do projeto exibe, a partir dos dados calculados pelo backend:

- distância total planejada (soma de todas as faixas);
- distância executada (soma das faixas marcadas como executadas);
- quantidade de faixas executadas sobre o total;
- percentual de execução, com barra de progresso.

O backend retorna todas as distâncias em **metros**; a conversão para
quilômetros acontece em `src/utils/formatarDistancia.js`, que exibe valores
abaixo de 1 km em metros para não perder legibilidade em faixas curtas.

Ao marcar ou desmarcar uma faixa como executada, o projeto é recarregado e o
resumo é recalculado. A barra de progresso reflete a mudança imediatamente.

## Arquitetura do Electron

O Electron separa a aplicação em processos com permissões distintas:

- **Processo principal** (`electron/main.js`) — roda em Node.js, com acesso
  ao sistema operacional. Responsável por criar e gerenciar a janela.
- **Processo de renderização** (renderer) — o React, rodando em um webview
  isolado, **sem** acesso direto ao Node.
- **Preload** (`electron/preload.js`) — expõe explicitamente ao renderer
  apenas o que for necessário, via `contextBridge`.

Essa separação (`contextIsolation: true`, `nodeIntegration: false`) evita que
código carregado na página acesse livremente o sistema de arquivos do usuário.

Como o backend é uma API HTTP local, o React chama os endpoints diretamente
via `fetch`, sem precisar passar pelo processo principal, por isso o preload
é intencionalmente enxuto. Se futuramente for necessário abrir o seletor de
arquivos nativo do sistema, é ali que a ponte seria adicionada.

## Pré-requisitos

- Node.js 18+
- Backend rodando em `http://localhost:8000`

## Como rodar

```bash
npm install
npm run dev
```

A janela do Electron abre automaticamente, com hot reload: alterações em
`src/` recarregam a interface, e alterações em `electron/` reiniciam o app.

> A URL do backend está definida em `src/api/cliente.js` (`URL_BASE`).

## Scripts

| Comando           | Descrição                                     |
|-------------------|-----------------------------------------------|
| `npm run dev`     | Ambiente de desenvolvimento com hot reload    |
| `npm run build`   | Build de produção do React                    |
| `npm run lint`    | Análise estática com ESLint                   |

## Camada de API

Toda comunicação HTTP passa por `src/api/cliente.js`, que centraliza:

- a URL base do backend;
- a conversão dos erros da API (`{ "mensagem": "..." }`) em `Error` com
  mensagem pronta para exibição;
- o tratamento de falha de conexão (backend fora do ar), com mensagem
  específica em vez do erro genérico de rede;
- respostas `204 No Content` (usadas nas exclusões), que não têm corpo.

Isso evita `fetch` espalhado pelos componentes e mantém o tratamento de erro
consistente em toda a aplicação.

## Feedback ao usuário

Toda operação (cadastro, importação, alteração de estado, exclusão) resulta
em uma mensagem de sucesso ou erro exibida no topo da tela, via o hook
`useMensagem` e o componente `Mensagem`.

Na importação de faixas, as linhas rejeitadas pelo backend são listadas
individualmente com o número da linha e o motivo da rejeição, permitindo
corrigir o arquivo de entrada sem adivinhação.

## Tema

As cores ficam centralizadas em `src/theme/cores.js`. Os componentes importam
a paleta em vez de repetir hex codes, de modo que ajustar o tema exige
alteração em um único arquivo.