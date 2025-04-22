// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  selectFolder: () => ipcRenderer.invoke('select-folder')
});
