const customToolbar = {
  template: '#toolbar',
  props: ['title', 'action', 'pay']
};

const homePage = {
  template: '#home',
  props: ['toggleMenu','payMenu'],
  components: { customToolbar }
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
        Fault: 'Fault Reporting',
        Profile: 'Profile'
      },
      openSide: false
    };
  },
  components: {
    Home: homePage,
    Food: foodPage,
    Bus: tempPage,
    Rental: tempPage,
    Library: tempPage,
    Booking: tempPage,
    Clinic: tempPage,
    Fault: tempPage,
    Profile: tempPage
  }
});

/**/