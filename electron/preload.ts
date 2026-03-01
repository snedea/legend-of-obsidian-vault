import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  selectVaultFolder: (): Promise<string | null> => ipcRenderer.invoke('select-vault-folder'),
  getBackendPort: (): Promise<number> => ipcRenderer.invoke('get-backend-port'),
  showTrafficLights: (): void => ipcRenderer.send('show-traffic-lights'),
  hideTrafficLights: (): void => ipcRenderer.send('hide-traffic-lights'),
});
