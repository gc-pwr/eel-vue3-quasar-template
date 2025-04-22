// src/electron/bundle-main.js - Special version for PyInstaller bundle
const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// Handle ICU data issues in PyInstaller bundles
if (process.env.PYINSTALLER_TEMP_FOLDER) {
    // If running from PyInstaller bundle
    app.setPath('userData', path.join(process.env.PYINSTALLER_TEMP_FOLDER, 'userData'));

    // Tell Electron where to find its resources
    if (fs.existsSync(path.join(process.env.PYINSTALLER_TEMP_FOLDER, 'resources'))) {
        process.env.ELECTRON_RESOURCES_PATH = path.join(process.env.PYINSTALLER_TEMP_FOLDER, 'resources');
    }

    // Tell Electron where to find locales
    if (fs.existsSync(path.join(process.env.PYINSTALLER_TEMP_FOLDER, 'locales'))) {
        process.env.ELECTRON_LOCALES_PATH = path.join(process.env.PYINSTALLER_TEMP_FOLDER, 'locales');
    }
}

// Keep a global reference of the window object
let mainWindow;

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: path.join(process.env.PYINSTALLER_TEMP_FOLDER || __dirname, 'web', 'icon.ico'),
    });

    // Get the URL from command line arguments or use a default
    // Eel passes the URL as the last command line argument
    const url = process.argv[process.argv.length - 1].startsWith('http')
        ? process.argv[process.argv.length - 1]
        : 'http://localhost:27000/index.html';

    console.log('Loading URL:', url);

    // Load the URL
    mainWindow.loadURL(url);

    // Emitted when the window is closed
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

ipcMain.handle('select-file', async (event) => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: []
    });

    if (canceled) {
        return null;
    } else {
        return filePaths[0];
    }
});

// Handle folder selection
ipcMain.handle('select-folder', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openDirectory']
    });

    if (result.canceled) {
        return null;
    } else {
        return result.filePaths[0];
    }
});

// This method will be called when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed
app.on('window-all-closed', function () {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) createWindow();
});