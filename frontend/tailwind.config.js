/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Educrat Theme Colors
        primary: {
          50: '#f3f0ff',
          100: '#ede8ff',
          200: '#ddd4ff',
          300: '#c4b2ff',
          400: '#a485ff',
          500: '#8558ff',
          600: '#5F3CFE',
          700: '#5729e8',
          800: '#4A3AC7',
          900: '#3d2a9e',
        },
        dark: {
          50: '#f7f3ff',
          100: '#ede8ff',
          200: '#ddd4ff',
          300: '#c4b2ff',
          400: '#a485ff',
          500: '#8558ff',
          600: '#1C0C45',
          700: '#161038',
          800: '#10082a',
          900: '#0a051c',
        },
        green: {
          50: '#f0fdf9',
          100: '#ccfdf0',
          200: '#99fbe4',
          300: '#5df5d5',
          400: '#26e7c2',
          500: '#00FF9D',
          600: '#00d882',
          700: '#00b069',
          800: '#008a54',
          900: '#006d46',
        },
        blue: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#5E5DF0',
          600: '#4c46d8',
          700: '#3730a3',
          800: '#1e1b8a',
          900: '#1e3a8a',
        },
        gray: {
          50: '#F9FAFB',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6B7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        display: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'large': '0 10px 40px -10px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'bounce-light': 'bounceLight 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        bounceLight: {
          '0%, 20%, 53%, 80%, 100%': { transform: 'translate3d(0,0,0)' },
          '40%, 43%': { transform: 'translate3d(0, -8px, 0)' },
          '70%': { transform: 'translate3d(0, -4px, 0)' },
          '90%': { transform: 'translate3d(0, -2px, 0)' },
        },
      },
    },
  },
  plugins: [],
}
