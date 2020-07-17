import Vue from 'vue'
import VueFormulate from '@braid/vue-formulate'
Vue.use(VueFormulate)
import App from './App.vue'
import VueRouter from 'vue-router';
import { routes } from './routes';

Vue.use(VueRouter);


const router = new VueRouter({
  routes,
  mode: 'hash'
});

router.beforeEach(function (to, from, next) {
  window.scrollTo(0, 0);
  next();
});

new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
