import ImportadorDeFaixas from './ImportadorDeFaixas';
import TabelaDeFaixas from './TabelaDeFaixas';

/** Painel lateral com os detalhes do projeto selecionado e suas faixas. */
function PainelDoProjeto({
  projeto,
  linhasRejeitadas,
  aoImportar,
  aoAlternarEstado,
  aoExcluirFaixa,
}) {
  if (!projeto) {
    return (
      <p style={{ color: '#666', fontSize: 14 }}>
        Selecione um projeto na lista para ver suas faixas.
      </p>
    );
  }

  return (
    <div>
      <h2 style={{ margin: '0 0 4px', fontSize: 18 }}>
        {projeto.numero} — {projeto.nome}
      </h2>
      <p style={{ margin: '0 0 16px', color: '#666', fontSize: 13 }}>
        {projeto.faixas.length} faixa(s) cadastrada(s)
      </p>

      <ImportadorDeFaixas aoImportar={aoImportar} />

      {linhasRejeitadas.length > 0 && (
        <details style={{ marginBottom: 16, fontSize: 13 }}>
          <summary style={{ cursor: 'pointer', color: '#b06000' }}>
            {linhasRejeitadas.length} linha(s) rejeitada(s) na ultima importacao
          </summary>
          <ul style={{ margin: '8px 0 0', paddingLeft: 20, color: '#5f1410' }}>
            {linhasRejeitadas.map((linha, indice) => (
              <li key={indice}>
                {linha.numero_linha > 0 && <strong>Linha {linha.numero_linha}: </strong>}
                {linha.motivo}
              </li>
            ))}
          </ul>
        </details>
      )}

      <TabelaDeFaixas
        faixas={projeto.faixas}
        aoAlternarEstado={aoAlternarEstado}
        aoExcluir={aoExcluirFaixa}
      />
    </div>
  );
}

export default PainelDoProjeto;