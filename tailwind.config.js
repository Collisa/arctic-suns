module.exports = {
  purge: {
    content: ['./templates/*.html'],
    content: ['./templates/**/*.html'],
  },
  theme: {
    extend: {
      spacing: {
        '1/8': '12.5%',
      }
    },
  },
  variants: {
    backgroundColor: ['responsive', 'hover', 'focus', 'odd']
  },
  plugins: [
    require('@tailwindcss/ui'),
  ],
}
