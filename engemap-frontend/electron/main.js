import { app, BrowserWindow } from 'electron';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Em desenvolvimento, o Vite serve o React em um servidor local com hot reload.
// Em producao, carregamos o HTML ja compilado.
const urlDeDesenvolvimento = process.env.VITE_DEV_SERVER_URL;

function criarJanelaPrincipal() {
  const janela = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: 'Engemap',
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
      // Mantem o renderer isolado do Node: o React so acessa o que for
      // exposto explicitamente pelo preload.
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (urlDeDesenvolvimento) {
    janela.loadURL(urlDeDesenvolvimento);
  } else {
    janela.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(() => {
  criarJanelaPrincipal();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      criarJanelaPrincipal();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});