import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

const local = (path) => fileURLToPath(new URL(path, import.meta.url));

export default defineConfig({
  base: './',
  server: {
    fs: { allow: [local('./'), local('../mobile/assets/data/knowledge/'), local('../mobile/src/core/knowledge/')] },
  },
});

