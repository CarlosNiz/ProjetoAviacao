import { useState } from 'react';

function useMensagem() {
  const [mensagem, setMensagem] = useState({ tipo: null, texto: '' });

  function mostrarSucesso(texto) {
    setMensagem({ tipo: 'sucesso', texto });
  }

  function mostrarErro(texto) {
    setMensagem({ tipo: 'erro', texto });
  }

  function limpar() {
    setMensagem({ tipo: null, texto: '' });
  }

  return { mensagem, mostrarSucesso, mostrarErro, limpar };
}

export default useMensagem;