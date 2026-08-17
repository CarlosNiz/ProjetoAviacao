import { useState } from 'react';

import cores from '../theme/cores';

/** Formulario de cadastro de projeto: numero e nome sao obrigatorios. */
function FormularioNovoProjeto({ aoCriar }) {
  const [numero, setNumero] = useState('');
  const [nome, setNome] = useState('');
  const [salvando, setSalvando] = useState(false);

  async function submeter(evento) {
    evento.preventDefault();
    setSalvando(true);
    try {
      await aoCriar(numero.trim(), nome.trim());
      setNumero('');
      setNome('');
    } finally {
      setSalvando(false);
    }
  }

  const podeSalvar = numero.trim() !== '' && nome.trim() !== '' && !salvando;

  return (
    <form onSubmit={submeter} style={{ display: 'grid', gap: 8, marginBottom: 20 }}>
      <input
        value={numero}
        onChange={(e) => setNumero(e.target.value)}
        placeholder="Numero do projeto"
        maxLength={50}
        style={estiloDoCampo}
      />
      <input
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        placeholder="Nome do projeto"
        maxLength={255}
        style={estiloDoCampo}
      />
      <button type="submit" disabled={!podeSalvar} style={estiloDoBotao(podeSalvar)}>
        {salvando ? 'Salvando...' : 'Cadastrar projeto'}
      </button>
    </form>
  );
}

const estiloDoCampo = {
  padding: '8px 10px',
  border: `1px solid ${cores.borda}`,
  borderRadius: 6,
  fontSize: 14,
  background: cores.fundoElevado,
  color: cores.texto,
};

function estiloDoBotao(habilitado) {
  return {
    padding: '9px 12px',
    border: 'none',
    borderRadius: 6,
    fontSize: 14,
    color: '#fff',
    background: habilitado ? cores.primaria : cores.primariaDesabilitada,
    cursor: habilitado ? 'pointer' : 'not-allowed',
  };
}

export default FormularioNovoProjeto;