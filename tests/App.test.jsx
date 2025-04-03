import { render, screen } from '@testing-library/react'
import App from '../src/App'

test('renders dashboard link', () => {
  render(<App />)
  const linkElement = screen.getByText(/dashboard/i)
  expect(linkElement).toBeInTheDocument()
})