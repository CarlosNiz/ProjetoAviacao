import { useCallback, useEffect, useState } from 'react';

import { criarProjeto, excluirProjeto, listarProjetos, obterProjeto } from './api/projetos';
import { atualizarEstadoDaFaixa, excluirFaixa, importarFaixas } from './api/faixas';
import FormularioNovoProjeto from './components/FormularioNovoProjeto';
import ListaDeProjetos from './components/ListaDeProjetos';
import Mensagem from './components/Mensagem';
import PainelDoProjeto from './components/PainelDoProjeto';
import useMensagem from './hooks/useMensagem';

function App() {
  const [projetos, setProjetos] = useState([]);
  const [projetoSelecionado, setProjetoSelecionado] = useState(null);
  const [linhasRejeitadas, setLinhasRejeitadas] = useState([]);
  const { mensagem, mostrarSucesso, mostrarErro } = useMensagem();

  const recarregarProjetos = useCallback(async () => {
    try {
      setProjetos(await listarProjetos());
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }, []);

  useEffect(() => {
    recarregarProjetos();
  }, [recarregarProjetos]);

  async function selecionarProjeto(projetoId) {
    setLinhasRejeitadas([]);
    try {
      setProjetoSelecionado(await obterProjeto(projetoId));
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  async function cadastrarProjeto(numero, nome) {
    try {
      const projeto = await criarProjeto(numero, nome);
      await recarregarProjetos();
      mostrarSucesso(`Projeto '${projeto.numero}' cadastrado com sucesso.`);
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  async function removerProjeto(projeto) {
    const confirmado = window.confirm(
      `Excluir o projeto '${projeto.numero}' e todas as suas faixas?`
    );
    if (!confirmado) {
      return;
    }
    try {
      await excluirProjeto(projeto.id);
      if (projetoSelecionado?.id === projeto.id) {
        setProjetoSelecionado(null);
      }
      await recarregarProjetos();
      mostrarSucesso(`Projeto '${projeto.numero}' excluido com sucesso.`);
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  async function importar(arquivo) {
    try {
      const resultado = await importarFaixas(projetoSelecionado.id, arquivo);
      setLinhasRejeitadas(resultado.linhas_rejeitadas);
      await selecionarProjeto(projetoSelecionado.id);
      await recarregarProjetos();
      mostrarSucesso(resultado.mensagem);
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  async function alternarEstadoDaFaixa(faixa, executada) {
    try {
      await atualizarEstadoDaFaixa(projetoSelecionado.id, faixa.id, executada);
      await selecionarProjeto(projetoSelecionado.id);
      mostrarSucesso(
        `Faixa '${faixa.nome}' marcada como ${executada ? 'executada' : 'nao executada'}.`
      );
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  async function removerFaixa(faixa) {
    const confirmado = window.confirm(`Excluir a faixa '${faixa.nome}'?`);
    if (!confirmado) {
      return;
    }
    try {
      await excluirFaixa(projetoSelecionado.id, faixa.id);
      await selecionarProjeto(projetoSelecionado.id);
      mostrarSucesso(`Faixa '${faixa.nome}' excluida com sucesso.`);
    } catch (erro) {
      mostrarErro(erro.message);
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '16px 24px', borderBottom: '1px solid #e0e0e0' }}>
        <h1 style={{ margin: 0, fontSize: 20 }}>Engemap — Gerenciamento de Missoes</h1>
      </header>

      <div style={{ padding: '16px 24px 0' }}>
        <Mensagem tipo={mensagem.tipo} texto={mensagem.texto} />
      </div>

      <main style={{ flex: 1, display: 'grid', gridTemplateColumns: '340px 1fr', gap: 24, padding: '0 24px 24px', overflow: 'hidden' }}>
        <section style={{ overflowY: 'auto' }}>
          <h2 style={{ fontSize: 16, marginTop: 0 }}>Projetos</h2>
          <FormularioNovoProjeto aoCriar={cadastrarProjeto} />
          <ListaDeProjetos
            projetos={projetos}
            projetoSelecionadoId={projetoSelecionado?.id}
            aoSelecionar={selecionarProjeto}
            aoExcluir={removerProjeto}
          />
        </section>

        <section style={{ overflowY: 'auto' }}>
          <PainelDoProjeto
            projeto={projetoSelecionado}
            linhasRejeitadas={linhasRejeitadas}
            aoImportar={importar}
            aoAlternarEstado={alternarEstadoDaFaixa}
            aoExcluirFaixa={removerFaixa}
          />
        </section>
      </main>
    </div>
  );
}

export default App;