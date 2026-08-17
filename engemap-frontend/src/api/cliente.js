/**
 * Cliente HTTP da API local do backend Engemap.
 *
 * Centraliza a URL base e o tratamento de erro: o backend sempre responde
 * erros de negocio no formato { mensagem: "..." }, entao convertemos isso
 * em uma Error com mensagem pronta para exibicao na interface.
 */

const URL_BASE = 'http://localhost:8000';

class ErroDaApi extends Error {
  constructor(mensagem, status) {
    super(mensagem);
    this.name = 'ErroDaApi';
    this.status = status;
  }
}

async function extrairMensagemDeErro(resposta) {
  try {
    const corpo = await resposta.json();
    return corpo.mensagem ?? `Erro ${resposta.status} ao comunicar com o servidor.`;
  } catch {
    return `Erro ${resposta.status} ao comunicar com o servidor.`;
  }
}

async function requisitar(caminho, opcoes = {}) {
  let resposta;
  try {
    resposta = await fetch(`${URL_BASE}${caminho}`, opcoes);
  } catch {
    // Falha de rede: normalmente significa que o backend nao esta rodando.
    throw new ErroDaApi(
      'Nao foi possivel conectar ao servidor. Verifique se o backend esta em execucao.',
      0
    );
  }

  if (!resposta.ok) {
    throw new ErroDaApi(await extrairMensagemDeErro(resposta), resposta.status);
  }

  // 204 No Content (usado nas exclusoes) nao possui corpo para desserializar.
  if (resposta.status === 204) {
    return null;
  }

  return resposta.json();
}

export { requisitar, ErroDaApi };