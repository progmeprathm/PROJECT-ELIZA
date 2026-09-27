/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        /* Zinc/Slate Premium Dark Theme Tokens */
        'md-sys-color-primary': '#e4e4e7',
        'md-sys-color-on-primary': '#09090b',
        'md-sys-color-primary-container': '#27272a',
        'md-sys-color-on-primary-container': '#fafafa',
        
        'md-sys-color-secondary': '#a1a1aa',
        'md-sys-color-on-secondary': '#09090b',
        'md-sys-color-secondary-container': '#3f3f46',
        'md-sys-color-on-secondary-container': '#f4f4f5',
        
        'md-sys-color-tertiary': '#a78bfa',
        'md-sys-color-on-tertiary': '#ffffff',
        'md-sys-color-tertiary-container': '#5b21b6',
        'md-sys-color-on-tertiary-container': '#ede9fe',
        
        'md-sys-color-error': '#fca5a5',
        'md-sys-color-on-error': '#450a0a',
        'md-sys-color-error-container': '#7f1d1d',
        'md-sys-color-on-error-container': '#fee2e2',
        
        'md-sys-color-background': '#09090b',
        'md-sys-color-on-background': '#fafafa',
        'md-sys-color-surface': '#09090b',
        'md-sys-color-on-surface': '#fafafa',
        'md-sys-color-surface-variant': '#18181b',
        'md-sys-color-on-surface-variant': '#a1a1aa',
        
        'md-sys-color-outline': '#52525b',
        'md-sys-color-outline-variant': '#27272a',
        
        /* Semantic ECOS Colors */
        'ecos-success': '#34d399',
        'ecos-success-container': 'rgba(52, 211, 153, 0.15)',
        'ecos-on-success-container': '#6ee7b7',
        
        'ecos-warning': '#fbbf24',
        'ecos-warning-container': 'rgba(251, 191, 36, 0.15)',
        'ecos-on-warning-container': '#fcd34d',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
