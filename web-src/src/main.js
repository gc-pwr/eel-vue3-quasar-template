import { createApp } from 'vue'

import { Quasar } from 'quasar'
import { Notify, Dark, Loading, Dialog } from 'quasar'

// Import icon libraries
import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/mdi-v7/mdi-v7.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

import App from './App.vue'
import router from './router'


const myApp = createApp(App)

myApp.use(Quasar, {
  plugins: {
    Dark,
    Notify,
    Loading,
    Dialog
  }, // import Quasar plugins and add here
  config: {
    dark: "auto"
  }
})

myApp.use(router)

myApp.mount('#app')
