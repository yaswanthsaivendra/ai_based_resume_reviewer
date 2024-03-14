/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*/templates/*/*.html', 
    './*/templates/*/*/*.html', 
    './*/*.py',
  ],
  theme: {
    extend: {
      colors : {
        'primary' : '#222f3e',
        'secondary' : '#008080',
        'teritiary' : '#A78295',
  
      },
    },
  },
  plugins: [],
}
