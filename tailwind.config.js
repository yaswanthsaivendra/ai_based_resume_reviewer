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
        'primary' : '#331D2C',
        'secondary' : '#3F2E3E',
        'teritiary' : '#A78295',
  
      },
    },
  },
  plugins: [],
}
