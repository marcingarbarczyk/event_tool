/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./apps/**/*.{html,js}"],
  theme: {
    extend: {
      container: {
        center: true,
        padding: '2rem', // Default padding for the container
      },
      minHeight: {
        '500px': '500px'
      }
    },
    screens: {
      sm: '480px', // Small screens
      md: '768px', // Medium screens
      lg: '1024px', // Large screens
      xl: '1110px', // Extra-large screens
      '2xl': '1110px', // Custom extra-large screens
    },
  },
  plugins: []
}

