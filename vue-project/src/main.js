import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import Vue from  'vue' 
import { BootstrapVue, IconsPlugin, ModalPlugin} from  'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import * as bootstrap from 'bootstrap'
import '@/scss/styles.scss'

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);


Vue.use(ModalPlugin)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)


app.mount('#app');
