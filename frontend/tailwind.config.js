/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{js,jsx,ts,tsx}'],
    theme: {
        extend: {
            backgroundColor: {
                primary: '#F9F7F7',
                secondary: '#DBE2EF'
            // Add other colors as needed
            },
            textColor: {
                primary: '#112D4E',
                secondary: '#3F72AF',
                highlight: '#c251ab'
            // Add other colors as needed
            }
        }
    },
    plugins: []
}
