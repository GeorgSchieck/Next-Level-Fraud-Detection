/**
 * Created by raf on 10.11.2017.
 */
import about from './about.vue';
import contact from './contact.vue';
import hero from './hero.vue';
import impressum from './impressum.vue';
import agb from './agb.vue';
import datenschutz from './datenschutz.vue';


export const routes = [
  {path: '/', component: hero},
  {path: '/contact', component: contact},
  {path: '/about', component: about},
  {path: '/impressum', component: impressum},
  {path: '/agb', component: agb},
  {path: '/datenschutz', component: datenschutz}

  // {path: '/stats', component: stats, beforeEnter: ((to, from, next) => {
  //   if (store.getters.getAuth === true) {
  //     next();
  //   }
  //   else {
  //     next({ path: '/login' });
  //   }
  // })
  // },
  // {path: '/logout', component: logout, beforeEnter: ((to, from, next) => {
  //   if (store.getters.getAuth === true) {
  //     next();
  //   }
  // })
  // },
];

export default routes

