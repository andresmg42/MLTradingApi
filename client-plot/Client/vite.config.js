import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(),tailwindcss(),],
  server: {
    host: '0.0.0.0', 
    port: 5173,
    allowedHosts: ['ec2-34-203-237-227.compute-1.amazonaws.com'],
  },
})
