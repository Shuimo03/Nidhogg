import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { HeroUIProvider } from '@heroui/react'
import './index.css'
import App from './App.tsx'

// Initialize theme synchronously before React renders
function initTheme() {
  if (typeof window === 'undefined') return
  
  const saved = window.localStorage.getItem('nidhogg.theme') as 'system' | 'light' | 'dark' | null
  const scheme = saved ?? 'system'
  
  const media = window.matchMedia('(prefers-color-scheme: dark)')
  const isDark = scheme === 'dark' || (scheme === 'system' && media.matches)
  
  const html = document.documentElement
  if (isDark) {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
  
  // Set color-scheme CSS property for better browser support
  html.style.colorScheme = isDark ? 'dark' : 'light'
}

// Apply theme before rendering
initTheme()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <HeroUIProvider>
      <App />
    </HeroUIProvider>
  </StrictMode>,
)
