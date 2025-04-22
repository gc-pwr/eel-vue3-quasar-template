# -*- mode: python ; coding: utf-8 -*-
import site
import os
import glob
import platform
import importlib


# Add Electron folder with all necessary files
electron_datas = []
electron_binaries = []

if platform.system() == 'Windows':
    # Windows: Include the entire electron folder
    electron_dist = os.path.join('web-src', 'node_modules', 'electron', 'dist')
    if os.path.exists(electron_dist):
        for root, dirs, files in os.walk(electron_dist):
            for file in files:
                if file.endswith('.dll') or file == 'electron.exe':
                    # Binaries go to binaries
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), electron_dist)
                    target_path = os.path.join('electron', rel_path) if rel_path != '.' else 'electron'
                    electron_binaries.append((full_path, target_path))
                else:
                    # Other files go to datas
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), electron_dist)
                    target_path = os.path.join('electron', rel_path) if rel_path != '.' else 'electron'
                    electron_datas.append((full_path, target_path))

elif platform.system() == 'Darwin':  # macOS
    electron_app = os.path.join('web-src', 'node_modules', 'electron', 'dist', 'Electron.app')
    if os.path.exists(electron_app):
        for root, dirs, files in os.walk(electron_app):
            for file in files:
                if file.endswith('.dylib') or 'Electron' in file and not file.endswith('.plist'):
                    # Binaries go to binaries
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), os.path.join('web-src', 'node_modules', 'electron', 'dist'))
                    target_path = os.path.join('electron', rel_path)
                    electron_binaries.append((full_path, target_path))
                else:
                    # Other files go to datas
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), os.path.join('web-src', 'node_modules', 'electron', 'dist'))
                    target_path = os.path.join('electron', rel_path)
                    electron_datas.append((full_path, target_path))

else:  # Linux
    electron_dist = os.path.join('web-src', 'node_modules', 'electron', 'dist')
    if os.path.exists(electron_dist):
        for root, dirs, files in os.walk(electron_dist):
            for file in files:
                if file == 'electron' or file.endswith('.so'):
                    # Binaries go to binaries
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), electron_dist)
                    target_path = os.path.join('electron', rel_path) if rel_path != '.' else 'electron'
                    electron_binaries.append((full_path, target_path))
                else:
                    # Other files go to datas
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(os.path.dirname(full_path), electron_dist)
                    target_path = os.path.join('electron', rel_path) if rel_path != '.' else 'electron'
                    electron_datas.append((full_path, target_path))

eel_path = os.path.dirname(importlib.import_module('eel').__file__)
eel_js_path = os.path.join(eel_path, 'eel.js')


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=electron_binaries,
    datas=[(eel_js_path, 'eel'), ('web', 'web')] + electron_datas,
    hiddenimports=[
        'bottle_websocket',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    '.\\web-src\\public\\img.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10,280),
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='ElectronApp',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='.\\web-src\\public\\icon.ico',
)
