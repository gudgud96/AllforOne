const customToolbar = {
  template: '#toolbar',
  props: ['title', 'action', 'pay']
};

const homePage = {
  template: '#home',
  props: ['toggleMenu','payMenu'],
  components: { customToolbar },
  data() {
    return {
      spdVisible: true,
      spdOpen: false
    }
  },
  methods:{
    push: function(page) {
      this.$emit('push-page',page)
    }
  }
};

const foodPage = {
  template: '#food',
  props: ['toggleMenu','payMenu'],
  components: { customToolbar }
};

const tempPage = {
  template: '#temp',
  props: ['toggleMenu','payMenu','title','titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const libraryPage = {
  template: '#library',
  props: ['toggleMenu','payMenu','title','titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

Vue.options.delimiters= ["[[", "]]"]

app = new Vue({
  el: '#app',
  template: '#main',
  data() {
    return {
      currentPage: 'Home',
      pages: {
        Home: 'Home', 
        Food: 'Food Payment', 
        Bus: 'NTU Bus', 
        Rental: 'Scooter/Bike Rental', 
        Library: 'Library Functions', 
        Booking: 'Booking Facilities', 
        Clinic: 'Clinic Services',
        Fault: 'Fault Reporting'
      },
      imgsrc: {
        Home: 'static/src/event.png', 
        Food: 'static/src/food.png', 
        Bus: 'static/src/bus.png', 
        Rental: 'static/src/bike.png', 
        Library: 'static/src/library.png', 
        Booking: 'static/src/booking.png', 
        Clinic: 'static/src/clinic.png',
        Fault: 'static/src/faulty.png'
      },
      openSide: false
    };
  },
  components: {
    Home: homePage,
    Food: foodPage,
    Bus: tempPage,
    Rental: tempPage,
    Library: libraryPage,
    Booking: tempPage,
    Clinic: tempPage,
    Fault: tempPage
  }
});

/**/