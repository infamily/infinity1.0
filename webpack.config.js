var webpack = require('webpack');
var path = require('path');

module.exports = {
  entry: [
    './src/components/index.js' // Your appʼs entry point
  ],
  output: {
    path: path.join(__dirname, 'src/static/bundle'),
    filename: 'app.js'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loaders: ['react-hot', 'babel'],
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,
        loader: 'url?limit=100000&name=[name].[ext]'
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: '"production"'
    }
  })
  ]
};
