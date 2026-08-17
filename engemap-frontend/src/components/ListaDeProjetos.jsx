import cores from '../theme/cores';

/** Lista lateral de projetos, com selecao e exclusao. */
function ListaDeProjetos({ projetos, projetoSelecionadoId, aoSelecionar, aoExcluir }) {
  if (projetos.length === 0) {
    return (
      <p style={{ color: cores.textoSecundario, fontSize: 14 }}>
        Nenhum projeto cadastrado ainda.
      </p>
    );
  }

  return (
    <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 6 }}>
      {projetos.map((projeto) => {
        const selecionado = projeto.id === projetoSelecionadoId;
        return (
          <li
            key={projeto.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 8,
              padding: '10px 12px',
              borderRadius: 6,
              border: `1px solid ${selecionado ? cores.bordaDestaque : cores.borda}`,
              background: selecionado ? cores.selecionado : cores.fundoElevado,
            }}
          >
            <button
              onClick={() => aoSelecionar(projeto.id)}
              style={{
                flex: 1,
                textAlign: 'left',
                border: 'none',
                background: 'transparent',
                cursor: 'pointer',
                fontSize: 14,
                color: cores.texto,
              }}
            >
              <strong>{projeto.numero}</strong>
              <span style={{ color: cores.textoSecundario }}> — {projeto.nome}</span>
            </button>
            <button
              onClick={() => aoExcluir(projeto)}
              title="Excluir projeto"
              style={{
                border: 'none',
                background: 'transparent',
                color: cores.perigo,
                cursor: 'pointer',
                fontSize: 13,
              }}
            >
              excluir
            </button>
          </li>
        );
      })}
    </ul>
  );
}

export default ListaDeProjetos;