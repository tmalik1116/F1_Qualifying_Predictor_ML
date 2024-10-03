const path = require('path'); 
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './frontend/build/static/main.js', // Your main JavaScript file
  output: {
    path: path.resolve(__dirname, 'frontend/build/static'), // Output directory
    filename: 'bundle.js' // Output file name
  },
  module: {
    rules: [
      {
        test: /\.css$/i, // Match CSS files
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './frontend/build/index.html' // Your HTML template file
    })
  ]
};