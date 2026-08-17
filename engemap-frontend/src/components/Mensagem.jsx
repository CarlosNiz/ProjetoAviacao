import cores from '../theme/cores';

/** Exibe o feedback de sucesso ou erro da ultima operacao realizada. */
function Mensagem({ tipo, texto }) {
  if (!texto) {
    return null;
  }

  const paleta = {
    sucesso: { fundo: '#1c3326', borda: cores.sucesso, texto: '#a9e8bf' },
    erro: { fundo: '#3a1f1f', borda: cores.perigo, texto: '#f5b3b1' },
  };
  const cor = paleta[tipo] ?? paleta.erro;

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