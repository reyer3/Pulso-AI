import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeAll, vi } from 'vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Setup global mocks
beforeAll(() => {
  // Mock IntersectionObserver
  global.IntersectionObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }))

  // Mock ResizeObserver
  global.ResizeObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }))

  // Mock window.matchMedia
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(), // deprecated
      removeListener: vi.fn(), // deprecated
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  })

  // Mock environment variables for testing
  vi.stubEnv('VITE_API_URL', 'http://localhost:8000')
  vi.stubEnv('VITE_GRAPHQL_URL', 'http://localhost:8000/graphql')
  vi.stubEnv('VITE_APP_NAME', 'Pulso-AI Test')
  vi.stubEnv('VITE_ENVIRONMENT', 'test')
})

// Global test utilities
global.testUtils = {
  // Helper for creating mock data
  createMockClient: () => ({
    id: 'test-client',
    name: 'Test Client',
    config: {},
  }),
  
  // Helper for async testing
  waitFor: (callback: () => void, timeout = 1000) => {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error(`Timeout after ${timeout}ms`))
      }, timeout)
      
      try {
        callback()
        clearTimeout(timer)
        resolve(true)
      } catch (error) {
        clearTimeout(timer)
        reject(error)
      }
    })
  },
}

// Extend global types for TypeScript
declare global {
  var testUtils: {
    createMockClient: () => { id: string; name: string; config: object }
    waitFor: (callback: () => void, timeout?: number) => Promise<unknown>
  }
}
