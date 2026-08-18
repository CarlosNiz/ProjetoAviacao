import { app, BrowserWindow, Menu} from 'electron';
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

  Menu.setApplicationMenu(null);
  
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