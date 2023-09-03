/** @type {import('tailwindcss').Config} */
module.exports = {
    corePlugins:{
      preflight: false
    },
    content: ["_includes/*.html", "_layouts/*.html", "_posts/**/*.md","./*.md"],
    theme: {
      extend: {},
    },
    plugins: []
  }