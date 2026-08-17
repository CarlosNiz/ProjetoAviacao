function Mensagem({ tipo, texto }) {
  if (!texto) {
    return null;
  }

  const cores = {
    sucesso: { fundo: '#e6f4ea', borda: '#34a853', texto: '#1e4620' },
    erro: { fundo: '#fce8e6', borda: '#d93025', texto: '#5f1410' },
  };
  const cor = cores[tipo] ?? cores.erro;

  return (
    <div
      role="status"
      style={{
        background: cor.fundo,
        border: `1px solid ${cor.borda}`,
        color: cor.texto,
        borderRadius: 6,
        padding: '10px 14px',
        marginBottom: 16,
        fontSize: 14,
      }}
    >
      {texto}
    </div>
  );
}

export default Mensagem;