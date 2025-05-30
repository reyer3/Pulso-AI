import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

// Basic App component for development
function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-primary-600 mb-4">
          🚀 Pulso-AI
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Plataforma de Business Intelligence Multi-Cliente
        </p>
        <div className="bg-white rounded-lg p-6 shadow-soft max-w-md mx-auto">
          <h2 className="text-xl font-semibold mb-4">
            ✅ Entorno de Desarrollo Listo
          </h2>
          <ul className="text-left space-y-2 text-sm">
            <li>✅ React 18 + TypeScript</li>
            <li>✅ TailwindCSS configurado</li>
            <li>✅ Vite para desarrollo rápido</li>
            <li>✅ GraphQL con Apollo Client</li>
            <li>✅ Tests con Vitest</li>
          </ul>
        </div>
        <p className="text-sm text-gray-500 mt-6">
          Phase 0: Fundación completada ✅
        </p>
      </div>
    </div>
  )
}

// Mount the app
const root = ReactDOM.createRoot(document.getElementById('root')!)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
