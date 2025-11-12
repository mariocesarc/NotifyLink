/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./core/templates/**/*.html",
    "./links/templates/**/*.html", 
    "./analytics/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          lightlight: '#f4f2ff',
          light: '#a78bfa',
          DEFAULT: '#7c3aed',
          dark: '#4c1d95',
        },
      },
    },
  },
  plugins: [],
}