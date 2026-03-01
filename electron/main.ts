import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import { startBackend, stopBackend, getBackendPort } from './python';

let mainWindow: BrowserWindow | null = null;

const isDev = !app.isPackaged;

async function createWindow(): Promise<void> {
  // Start Python backend first
  console.log('Starting backend...');
  try {
    await startBackend();
    console.log(`Backend running on port ${getBackendPort()}`);
  } catch (err) {
    console.error('Failed to start backend:', err);
    dialog.showErrorBox('Backend Error', 'Failed to start the game backend. Please check Python installation.');
    app.quit();
    return;
  }

  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    minWidth: 700,
    minHeight: 500,
    backgroundColor: '#000000',
    titleBarStyle: 'hiddenInset',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.setTitle('Legend of the Obsidian Vault');

  // Inject backend port into renderer before loading content
  mainWindow.webContents.on('did-finish-load', () => {
    mainWindow?.webContents.executeJavaScript(
      `window.__BACKEND_PORT__ = ${getBackendPort()};`
    );
  });

  if (isDev) {
    // Dev: load Vite dev server
    await mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  } else {
    // Prod: frontend/dist is packaged at app root level
    // __dirname = electron/dist/, app root = __dirname/../..
    // But in asar: use app.getAppPath() which points to the app root
    await mainWindow.loadFile(path.join(app.getAppPath(), 'frontend', 'dist', 'index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// IPC handlers
ipcMain.handle('select-vault-folder', async () => {
  if (!mainWindow) return null;
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
    title: 'Select Obsidian Vault Folder',
  });
  if (result.canceled || result.filePaths.length === 0) return null;
  return result.filePaths[0];
});

ipcMain.handle('get-backend-port', () => getBackendPort());

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  stopBackend();
  app.quit();
});

app.on('before-quit', () => {
  stopBackend();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
