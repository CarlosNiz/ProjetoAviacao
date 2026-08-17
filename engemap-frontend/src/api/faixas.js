/** Chamadas da API relacionadas a Faixas dentro de um Projeto. */
import { requisitar } from './cliente';

function listarFaixas(projetoId) {
  return requisitar(`/projetos/${projetoId}/faixas`);
}

function importarFaixas(projetoId, arquivo) {
  const dadosDoFormulario = new FormData();
  dadosDoFormulario.append('arquivo', arquivo);

  // Nao definimos Content-Type manualmente: o browser precisa gerar o
  // boundary do multipart/form-data automaticamente.
  return requisitar(`/projetos/${projetoId}/faixas/importar`, {
    method: 'POST',
    body: dadosDoFormulario,
  });
}

function atualizarEstadoDaFaixa(projetoId, faixaId, executada) {
  return requisitar(`/projetos/${projetoId}/faixas/${faixaId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ executada }),
  });
}

function excluirFaixa(projetoId, faixaId) {
  return requisitar(`/projetos/${projetoId}/faixas/${faixaId}`, { method: 'DELETE' });
}

export { listarFaixas, importarFaixas, atualizarEstadoDaFaixa, excluirFaixa };