/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{js,jsx,ts,tsx}'],
    theme: {
        extend: {
            backgroundColor: {
                primary: '#062F4F',
                secondary: '#B82601',
                highlight: '#813772'
            // Add other colors as needed
            },
            textColor: {
                primary: '#112D4E',
                secondary: '#3F72AF',
                highlight: '#813772'
            // Add other colors as needed
            }
        }
    },
    plugins: []
}
