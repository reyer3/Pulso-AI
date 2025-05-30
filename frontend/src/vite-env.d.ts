/// <reference types="vite/client" />

// Vite environment variables type definitions
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_GRAPHQL_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_LOG_LEVEL: string
  readonly VITE_ENVIRONMENT: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
