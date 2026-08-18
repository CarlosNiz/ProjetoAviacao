import cores from '../theme/cores';
import formatarDistancia from '../utils/formatarDistancia';

/** Progresso de execucao do projeto: distancias planejada, executada e percentual. */
function ResumoDeExecucao({ resumo }) {
  const percentual = resumo.percentual_executado;

  return (
    <div
      style={{
        border: `1px solid ${cores.borda}`,
        borderRadius: 8,
        padding: 16,
        marginBottom: 16,
        background: cores.fundoElevado,
      }}
    >
      <div style={{ display: 'flex', gap: 24, marginBottom: 14, flexWrap: 'wrap' }}>
        <Indicador
          rotulo="Distancia planejada"
          valor={formatarDistancia(resumo.distancia_total_metros)}
        />
        <Indicador
          rotulo="Distancia executada"
          valor={formatarDistancia(resumo.distancia_executada_metros)}
          destaque
        />
        <Indicador
          rotulo="Faixas executadas"
          valor={`${resumo.faixas_executadas} de ${resumo.total_de_faixas}`}
        />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div
          style={{
            flex: 1,
            height: 10,
            borderRadius: 5,
            background: cores.fundoSutil,
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              width: `${percentual}%`,
              height: '100%',
              background: cores.sucesso,
              transition: 'width 0.3s ease',
            }}
          />
        </div>
        <strong style={{ fontSize: 14, color: cores.sucesso, minWidth: 52, textAlign: 'right' }}>
          {percentual.toFixed(1)}%
        </strong>
      </div>
    </div>
  );
}

function Indicador({ rotulo, valor, destaque = false }) {
  return (
    <div>
      <p style={{ margin: 0, fontSize: 12, color: cores.textoSecundario }}>{rotulo}</p>
      <p
        style={{
          margin: '2px 0 0',
          fontSize: 17,
          fontWeight: 600,
          color: destaque ? cores.sucesso : cores.texto,
        }}
      >
        {valor}
      </p>
    </div>
  );
}

export default ResumoDeExecucao;