const { defineConfig } = require('@vue/cli-service')
const { VuetifyPlugin } = require('webpack-plugin-vuetify')
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/static/notifapi/vue-ui/dist/', // Should be STATIC_URL + path/to/build
  outputDir: path.resolve(__dirname, '../myproj/notifapi/static/notifapi/vue-ui/dist/'),
  filenameHashing: false, // Django will hash file names, not webpack
  runtimeCompiler: true,
  devServer: {
    hot:false,
    devMiddleware: {
      writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
    },
    proxy: {
      '/websocket': {
        target: 'http://127.0.0.1:8001',
        ws: true,
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    plugins: [
      new VuetifyPlugin({autoImport: true, styles: true})
    ]
  }
})
