import { useMemo, useState } from 'react';

import cores from '../theme/cores';

/** Tabela de faixas do projeto, com ordenacao por nome, alteracao de estado e exclusao. */
function TabelaDeFaixas({ faixas, aoAlternarEstado, aoExcluir }) {
  const [ordemCrescente, setOrdemCrescente] = useState(true);

  // localeCompare com 'pt-BR' e numeric: true garante que 'faixa2' venha
  // antes de 'faixa10' (comparacao alfabetica pura inverteria os dois).
  const faixasOrdenadas = useMemo(() => {
    const copia = [...faixas];
    copia.sort((a, b) => {
      const comparacao = a.nome.localeCompare(b.nome, 'pt-BR', { numeric: true });
      return ordemCrescente ? comparacao : -comparacao;
    });
    return copia;
  }, [faixas, ordemCrescente]);

  if (faixas.length === 0) {
    return (
      <p style={{ color: cores.textoSecundario, fontSize: 14 }}>
        Nenhuma faixa importada neste projeto ainda.
      </p>
    );
  }

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
      <thead>
        <tr style={{ background: cores.fundoElevado, textAlign: 'left' }}>
          <th style={estiloDaCelula}>
            <button
              onClick={() => setOrdemCrescente((atual) => !atual)}
              title="Ordenar por nome"
              style={{
                border: 'none',
                background: 'transparent',
                color: cores.texto,
                cursor: 'pointer',
                font: 'inherit',
                fontWeight: 'bold',
                padding: 0,
                display: 'flex',
                alignItems: 'center',
                gap: 4,
              }}
            >
              Nome
              <span style={{ color: cores.textoSecundario, fontSize: 11 }}>
                {ordemCrescente ? '▲' : '▼'}
              </span>
            </button>
          </th>
          <th style={estiloDaCelula}>Lat. A</th>
          <th style={estiloDaCelula}>Lon. A</th>
          <th style={estiloDaCelula}>Lat. B</th>
          <th style={estiloDaCelula}>Lon. B</th>
          <th style={estiloDaCelula}>Executada</th>
          <th style={estiloDaCelula}></th>
        </tr>
      </thead>
      <tbody>
        {faixasOrdenadas.map((faixa) => (
          <tr key={faixa.id}>
            <td style={estiloDaCelula}>{faixa.nome}</td>
            <td style={estiloDaCelula}>{faixa.latitude_a}</td>
            <td style={estiloDaCelula}>{faixa.longitude_a}</td>
            <td style={estiloDaCelula}>{faixa.latitude_b}</td>
            <td style={estiloDaCelula}>{faixa.longitude_b}</td>
            <td style={estiloDaCelula}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <input
                  type="checkbox"
                  checked={faixa.executada}
                  onChange={(e) => aoAlternarEstado(faixa, e.target.checked)}
                />
                <span style={{ color: faixa.executada ? cores.sucesso : cores.textoSecundario }}>
                  {faixa.executada ? 'Executada' : 'Nao executada'}
                </span>
              </label>
            </td>
            <td style={estiloDaCelula}>
              <button
                onClick={() => aoExcluir(faixa)}
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
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const estiloDaCelula = {
  padding: '8px 10px',
  borderBottom: `1px solid ${cores.borda}`,
  color: cores.texto,
};

export default TabelaDeFaixas;