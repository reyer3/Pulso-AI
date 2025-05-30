import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Enable React Fast Refresh
      fastRefresh: true,
    }),
  ],
  
  // Path resolution
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@graphql': path.resolve(__dirname, './src/graphql'),
      '@types': path.resolve(__dirname, './src/types'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@assets': path.resolve(__dirname, './src/assets'),
    },
  },

  // Development server configuration
  server: {
    port: 3000,
    host: true, // Para Docker
    open: false, // No abrir browser automáticamente
    cors: true,
    proxy: {
      // Proxy para desarrollo con backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/graphql': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },

  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'esbuild',
    target: 'esnext',
    
    // Bundle splitting para mejor performance
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks
          react: ['react', 'react-dom'],
          router: ['react-router-dom'],
          apollo: ['@apollo/client', 'graphql'],
          ui: ['@radix-ui/react-dropdown-menu', '@radix-ui/react-dialog'],
          charts: ['recharts'],
          forms: ['react-hook-form', '@hookform/resolvers', 'zod'],
          utils: ['date-fns', 'clsx', 'tailwind-merge'],
        },
      },
    },
    
    // Optimize dependencies
    chunkSizeWarningLimit: 1000,
  },

  // Preview configuration (para testing de build)
  preview: {
    port: 3001,
    host: true,
    cors: true,
  },

  // CSS configuration
  css: {
    postcss: './postcss.config.js',
    devSourcemap: true,
  },

  // Environment variables
  envPrefix: 'VITE_',
  envDir: '../', // Para leer .env del root

  // Dependency optimization
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      '@apollo/client',
      'graphql',
      'recharts',
      'react-hook-form',
      'zod',
      'date-fns',
      'clsx',
      'tailwind-merge',
      'lucide-react',
    ],
    exclude: [
      // Exclude packages that should not be pre-bundled
    ],
  },

  // Testing configuration (para Vitest)
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/main.tsx',
        'src/vite-env.d.ts',
      ],
    },
  },

  // Performance optimizations
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' },
  },
})
