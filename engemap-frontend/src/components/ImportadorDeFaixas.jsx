import { useRef, useState } from 'react';

import cores from '../theme/cores';

/** Seleciona um arquivo .txt e dispara a importacao de faixas no projeto. */
function ImportadorDeFaixas({ aoImportar }) {
  const [arquivoSelecionado, setArquivoSelecionado] = useState(null);
  const [importando, setImportando] = useState(false);
  const campoDeArquivo = useRef(null);

  async function importar() {
    if (!arquivoSelecionado) {
      return;
    }
    setImportando(true);
    try {
      await aoImportar(arquivoSelecionado);
      setArquivoSelecionado(null);
      // Limpa o input nativo: sem isso, selecionar o mesmo arquivo
      // novamente nao dispararia o evento onChange.
      if (campoDeArquivo.current) {
        campoDeArquivo.current.value = '';
      }
    } finally {
      setImportando(false);
    }
  }

  const podeImportar = arquivoSelecionado && !importando;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        padding: 12,
        border: `1px dashed ${cores.borda}`,
        borderRadius: 6,
        marginBottom: 16,
        background: cores.fundoSutil,
      }}
    >
      <input
        ref={campoDeArquivo}
        type="file"
        accept=".txt"
        onChange={(e) => setArquivoSelecionado(e.target.files?.[0] ?? null)}
        style={{ fontSize: 14, color: cores.texto }}
      />
      <button
        onClick={importar}
        disabled={!podeImportar}
        style={{
          padding: '8px 14px',
          border: 'none',
          borderRadius: 6,
          fontSize: 14,
          color: '#fff',
          background: podeImportar ? cores.primaria : cores.primariaDesabilitada,
          cursor: podeImportar ? 'pointer' : 'not-allowed',
        }}
      >
        {importando ? 'Importando...' : 'Importar faixas'}
      </button>
    </div>
  );
}

export default ImportadorDeFaixas;