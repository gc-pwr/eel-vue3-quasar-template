import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
import { resolve } from 'path';
import fs from 'fs';


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),

    quasar({
    }),

    {
    name: 'copy-electron-for-bundle',
    closeBundle() {
      // Create directory if it doesn't exist
      const electronDir = resolve(__dirname, '../web/electron');
      if (!fs.existsSync(electronDir)) {
        fs.mkdirSync(electronDir, { recursive: true });
      }

      // Copy the Electron main file with a fixed name
      fs.copyFileSync(
        resolve(__dirname, 'src/electron/index.cjs'),
        resolve(electronDir, 'bundle-main.js')
      );

      // If preload.js exists, copy it too
      const preloadPath = resolve(__dirname, 'src/electron/preload.js');
      if (fs.existsSync(preloadPath)) {
        fs.copyFileSync(
          preloadPath,
          resolve(electronDir, 'preload.js')
        );
      }
    }
  }
  ],
  build: {
    outDir: "../web",
  },
});
