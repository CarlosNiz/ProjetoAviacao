import { useEffect, useState } from 'react';
import { listarProjetos } from './api/projetos';

function App() {
  const [projetos, setProjetos] = useState([]);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    listarProjetos()
      .then(setProjetos)
      .catch((e) => setErro(e.message));
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Engemap</h1>
      {erro && <p style={{ color: 'crimson' }}>{erro}</p>}
      <pre>{JSON.stringify(projetos, null, 2)}</pre>
    </div>
  );
}

export default App;