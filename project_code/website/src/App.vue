<template>
  <div>
    <div id="preloader"></div>
<raf-nav></raf-nav>
    <!--==========================
    Hero Section
    ============================-->


    <!--==========================
    Header Section
    ============================-->

    <!-- #header -->

    <!--==========================
    About Section
    ============================-->

<router-view></router-view>
    <!--==========================
    Services Section
    ============================-->


    <!--==========================
    Subscrbe Section
    ============================-->


    <!--==========================
    Porfolio Section
    ============================-->


    <!--==========================
    Testimonials Section
    ============================-->


    <!--==========================
    Team Section
    ============================-->


    <!--==========================
    Contact Section
    ============================-->


    <!--==========================
    Footer
  ============================-->
<raf-footer></raf-footer>
    <!-- #footer -->

    <a href="#" class="back-to-top"><i class="fa fa-chevron-up"></i></a>
  </div>

</template>

<script>
  import Header from './header.vue';
  import Footer from './footer.vue';
  import Hero from './hero.vue';

  export default {
    name: 'app',
    components: {
        'raf-nav' : Header,
      'raf-footer' : Footer,
      'raf-hero' : Hero
    },
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    }
  }
</script>

