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
    Mensagem.jsx        # feedback de sucesso/erro
    PainelDoProjeto.jsx
    TabelaDeFaixas.jsx
  hooks/
    useMensagem.js      # centraliza o estado de feedback ao usuário
  theme/
    cores.js            # paleta do tema escuro
  App.jsx               # composição da tela e orquestração das chamadas
  main.jsx              # ponto de entrada do React
```

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
via `fetch`, sem precisar passar pelo processo principal por isso o preload
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

## Tema

As cores ficam centralizadas em `src/theme/cores.js`. Os componentes importam
a paleta em vez de repetir hex codes, de modo que ajustar o tema exige
alteração em um único arquivo.

## Próximos passos sugeridos

- Empacotamento em instalador desktop (`electron-builder`) para distribuição
- Extrair a URL do backend para variável de ambiente, em vez de constante
- Testes de componente (React Testing Library)