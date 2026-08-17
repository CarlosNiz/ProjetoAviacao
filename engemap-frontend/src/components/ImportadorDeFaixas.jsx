import { useRef, useState } from 'react';

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

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        padding: 12,
        border: '1px dashed #bbb',
        borderRadius: 6,
        marginBottom: 16,
      }}
    >
      <input
        ref={campoDeArquivo}
        type="file"
        accept=".txt"
        onChange={(e) => setArquivoSelecionado(e.target.files?.[0] ?? null)}
        style={{ fontSize: 14 }}
      />
      <button
        onClick={importar}
        disabled={!arquivoSelecionado || importando}
        style={{
          padding: '8px 14px',
          border: 'none',
          borderRadius: 6,
          fontSize: 14,
          color: '#fff',
          background: arquivoSelecionado && !importando ? '#1a73e8' : '#9bb8e3',
          cursor: arquivoSelecionado && !importando ? 'pointer' : 'not-allowed',
        }}
      >
        {importando ? 'Importando...' : 'Importar faixas'}
      </button>
    </div>
  );
}

export default ImportadorDeFaixas;