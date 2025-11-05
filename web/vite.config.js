import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    strictPort: true, // Falla si el puerto está ocupado en lugar de usar otro
    watch: {
      usePolling: true
    }
  }
})