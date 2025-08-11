import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Moo Climate Brand Colors (Minimalistic Usage)
        'moo-yellow': '#F7D774',
        'moo-green': '#2E5E4E',
        'sidebar-blue': '#69B8E5',
        
        // Minimalistic Color System - Light Theme Focus
        background: "#FFFFFF",
        foreground: "#171717",
        card: {
          DEFAULT: "#FFFFFF",
          foreground: "#171717",
        },
        popover: {
          DEFAULT: "#FFFFFF",
          foreground: "#171717",
        },
        primary: {
          DEFAULT: "#F7D774",
          foreground: "#171717",
        },
        secondary: {
          DEFAULT: "#FFFFFF",
          foreground: "#525252",
        },
        muted: {
          DEFAULT: "#FAFAFA",
          foreground: "#525252",
        },
        accent: {
          DEFAULT: "#F7D774",
          foreground: "#171717",
        },
        destructive: {
          DEFAULT: "#EF4444",
          foreground: "#FFFFFF",
        },
        border: "#E5E5E5",
        input: "#FFFFFF",
        ring: "#F7D774",
        
        // Extended Neutral Palette
        gray: {
          50: "#FAFAFA",
          100: "#F5F5F5", 
          200: "#E5E5E5",
          300: "#D4D4D4",
          400: "#A3A3A3",
          500: "#737373",
          600: "#525252",
          700: "#404040",
          800: "#262626",
          900: "#171717",
        },
        
        // Semantic Colors (Minimal Usage)
        success: "#22C55E",
        warning: "#F59E0B",
        error: "#EF4444",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        primary: ['Inter', 'system-ui', 'sans-serif'],
        secondary: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xs': ['11px', { lineHeight: '16px', letterSpacing: '0.02em', fontWeight: '500' }],
        'sm': ['12px', { lineHeight: '16px', fontWeight: '400' }],
        'base': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'lg': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'xl': ['18px', { lineHeight: '24px', fontWeight: '500' }],
        '2xl': ['20px', { lineHeight: '28px', fontWeight: '600' }],
        '3xl': ['24px', { lineHeight: '32px', fontWeight: '600', letterSpacing: '-0.01em' }],
        '4xl': ['32px', { lineHeight: '40px', fontWeight: '700', letterSpacing: '-0.02em' }],
      },
      spacing: {
        '18': '4.5rem',   // 72px
        '22': '5.5rem',   // 88px
        '26': '6.5rem',   // 104px
        '30': '7.5rem',   // 120px
      },
      borderRadius: {
        'none': '0',
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
        'xl': '12px',
        '2xl': '16px',
        'full': '9999px',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.02)',
        'minimal': '0 1px 3px 0 rgba(0, 0, 0, 0.02), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        'subtle': '0 2px 4px 0 rgba(0, 0, 0, 0.03), 0 1px 2px 0 rgba(0, 0, 0, 0.02)',
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-up": "slideUp 0.2s ease-out",
        "slide-down": "slideDown 0.2s ease-out",
        "scale-in": "scaleIn 0.2s ease-out",
        "pulse-subtle": "pulseSubtle 2s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(8px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDown: {
          "0%": { transform: "translateY(-8px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        scaleIn: {
          "0%": { transform: "scale(0.95)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
        pulseSubtle: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.8" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
