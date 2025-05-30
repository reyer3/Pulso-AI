import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import React from 'react'
import ReactDOM from 'react-dom/client'

// Simple test to verify setup is working
describe('Pulso-AI Frontend Setup', () => {
  it('should render without crashing', () => {
    const div = document.createElement('div')
    const root = ReactDOM.createRoot(div)
    
    const TestApp = () => (
      <div>
        <h1>Pulso-AI Test</h1>
        <p>Setup verification</p>
      </div>
    )
    
    expect(() => {
      root.render(<TestApp />)
    }).not.toThrow()
  })

  it('should have basic React functionality', () => {
    const TestComponent = () => (
      <div data-testid="test-component">
        <h1>Test Component</h1>
        <button>Test Button</button>
      </div>
    )

    render(<TestComponent />)
    
    expect(screen.getByTestId('test-component')).toBeDefined()
    expect(screen.getByText('Test Component')).toBeDefined()
    expect(screen.getByText('Test Button')).toBeDefined()
  })

  it('should verify environment is properly configured', () => {
    // Test that we're in test environment
    expect(import.meta.env).toBeDefined()
    
    // Test that basic DOM APIs are available
    expect(document).toBeDefined()
    expect(window).toBeDefined()
  })

  it('should have TypeScript support', () => {
    // This test will fail compilation if TypeScript isn't working
    const testFunction = (value: string): number => {
      return value.length
    }
    
    expect(testFunction('hello')).toBe(5)
    expect(typeof testFunction('test')).toBe('number')
  })
})

// Basic integration test
describe('Development Environment Integration', () => {
  it('should be able to create React elements', () => {
    const element = React.createElement('div', { id: 'test' }, 'Hello Pulso-AI')
    expect(element.type).toBe('div')
    expect(element.props.id).toBe('test')
    expect(element.props.children).toBe('Hello Pulso-AI')
  })

  it('should support ES6+ features', () => {
    // Arrow functions
    const arrow = () => 'arrow function works'
    expect(arrow()).toBe('arrow function works')

    // Template literals
    const name = 'Pulso-AI'
    expect(`Hello ${name}!`).toBe('Hello Pulso-AI!')

    // Destructuring
    const { length } = [1, 2, 3]
    expect(length).toBe(3)

    // Async/await (basic test)
    const asyncTest = async () => {
      const result = await Promise.resolve('async works')
      return result
    }
    
    return asyncTest().then(result => {
      expect(result).toBe('async works')
    })
  })
})
