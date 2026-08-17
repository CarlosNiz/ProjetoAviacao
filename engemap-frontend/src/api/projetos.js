/** Chamadas da API relacionadas a Projetos. */
import { requisitar } from './cliente';

function listarProjetos() {
  return requisitar('/projetos');
}

function obterProjeto(projetoId) {
  return requisitar(`/projetos/${projetoId}`);
}

function criarProjeto(numero, nome) {
  return requisitar('/projetos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ numero, nome }),
  });
}

function excluirProjeto(projetoId) {
  return requisitar(`/projetos/${projetoId}`, { method: 'DELETE' });
}

export { listarProjetos, obterProjeto, criarProjeto, excluirProjeto };