/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sand: {
          50: '#FDFBF7',
          100: '#F8F4EC',
          200: '#EFE6D8',
          300: '#E2D3BE',
          400: '#CDB99C',
          500: '#B69E7D',
          600: '#947D5F',
          700: '#735E44',
          800: '#4F3E2C',
          900: '#2E2318',
        },
        terracotta: {
          50: '#FDF6F3',
          100: '#FBEDE7',
          200: '#F6D7CB',
          300: '#EFAEA1',
          400: '#E47E68',
          500: '#C85A32',
          600: '#B54823',
          700: '#963818',
          800: '#7A2E14',
          900: '#4E1B0A',
        },
        clay: {
          50: '#FAF8F5',
          100: '#F4EFE6',
          200: '#EAE1D2',
          300: '#D7C7B0',
          400: '#BAA385',
          500: '#9D8362',
          600: '#7E6649',
          700: '#614E36',
          800: '#433423',
          900: '#261C12',
        },
        chai: {
          50: '#FAF7F2',
          100: '#F3ECE0',
          200: '#E5D6C1',
          300: '#D2BA99',
          400: '#BB996C',
          500: '#A47D4C',
          600: '#876339',
          700: '#6B4C2A',
          800: '#4B341D',
          900: '#2C1E10',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Lora', 'Georgia', 'serif'],
      },
      boxShadow: {
        'warm-sm': '0 1px 3px rgba(79, 62, 44, 0.05), 0 1px 2px rgba(79, 62, 44, 0.03)',
        'warm-md': '0 4px 12px rgba(79, 62, 44, 0.08), 0 2px 4px rgba(79, 62, 44, 0.04)',
        'warm-lg': '0 10px 25px -5px rgba(79, 62, 44, 0.1), 0 8px 10px -6px rgba(79, 62, 44, 0.05)',
        'warm-xl': '0 20px 35px -10px rgba(79, 62, 44, 0.12), 0 10px 15px -5px rgba(79, 62, 44, 0.06)',
        'glow-terracotta': '0 0 25px rgba(200, 90, 50, 0.35)',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'ripple': 'ripple 2s linear infinite',
      },
      keyframes: {
        ripple: {
          '0%': { transform: 'scale(0.8)', opacity: '1' },
          '100%': { transform: 'scale(2.2)', opacity: '0' },
        }
      }
    },
  },
  plugins: [],
}
