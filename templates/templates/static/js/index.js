const customToolbar = {
  template: '#toolbar',
  props: ['title', 'action']
};

const homePage = {
  template: '#home',
  props: ['toggleMenu'],
  components: { customToolbar }
};

const settingsPage = {
  template: '#settings',
  props: ['toggleMenu'],
  components: { customToolbar }
};

new Vue({
  el: '#app',
  template: '#main',
  data() {
    return {
      currentPage: 'home',
      pages: ['home', 'settings'],
      openSide: false
    };
  },
  components: {
    home: homePage,
    settings: settingsPage,
  }
});