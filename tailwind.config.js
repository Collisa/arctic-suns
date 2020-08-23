module.exports = {
  purge: {
    content: ['./templates/*.html'],
  },
  theme: {
    extend: {
      spacing: {
        '1/8': '12.5%',
      }
    },
  },
  variants: {},
  plugins: [
    require('@tailwindcss/ui'),
  ],
}
