import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/film': 'http://localhost:8000', //à modifier si le site est mis en prod
      '/note': 'http://localhost:8000',
      '/anime': 'http://localhost:8000',
    },
  },
});
