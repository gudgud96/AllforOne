const customToolbar = {
  template: '#toolbar',
  props: ['title', 'action', 'pay']
};

const homePage = {
  template: '#home',
  props: ['toggleMenu', 'payMenu'],
  components: { customToolbar },
  data() {
    return {
      spdVisible: true,
      spdOpen: false
    }
  },
  methods: {
    push: function (page) {
      this.$emit('push-page', page)
    }
  }
};

const foodPage = {
  template: '#food',
  props: ['toggleMenu', 'payMenu'],
  components: { customToolbar },
  methods: {
    createChart: function(){
      var randomScalingFactor = function () {
        return Math.round(Math.random() * 100);
      };

      var config = {
        type: 'pie',
        data: {
          datasets: [{
            data: [
              document.getElementById('ns').value,
              document.getElementById('ss').value,
              document.getElementById('quad').value,
              document.getElementById('mcd').value,
              document.getElementById('can2').value,

            ],
            backgroundColor: [
              window.chartColors.red,
              window.chartColors.orange,
              window.chartColors.yellow,
              window.chartColors.green,
              window.chartColors.blue,
            ],
            label: 'Dataset 1'
          }],
          labels: [
            'North Spine Canteen',
            'South Spine Canteen',
            'The Quad',
            "McDonald's",
            'Canteen 2'
          ]
        },
        options: {
          responsive: true,
          plugins: {
            datalabels: {
              formatter: (value, ctx) => {

                let sum = 0;
                let dataArr = ctx.chart.data.datasets[0].data;
                dataArr.map(data => {
                  sum += data;
                });
                let percentage = (value * 100 / sum).toFixed(2) + "%";
                return percentage;
              },
              color: '#fff',
            }
          }
        }
      };

      var config2 = {
        type: 'pie',
        data: {
          datasets: [{
            data: [
              30, 20, 20, 15, 15
            ],
            backgroundColor: [
              window.chartColors.red,
              window.chartColors.orange,
              window.chartColors.yellow,
              window.chartColors.green,
              window.chartColors.blue,
            ],
            label: 'Dataset 1'
          }],
          labels: [
            'North Spine Canteen',
            'South Spine Canteen',
            'The Quad',
            "McDonald's",
            'Canteen 2'
          ]
        },
        options: {
          responsive: true
        }
      };

      var ctx = document.getElementById('chart-area').getContext('2d');
      window.myPie = new Chart(ctx, config);
      var ctx2 = document.getElementById('chart-area-2').getContext('2d');
      window.myPie = new Chart(ctx2, config2);
    },
    post: function(){
      axios.post('/user', {
        firstName: 'Fred',
        lastName: 'Flintstone'
      })
      .then(function (response) {
        $ons.notification.alert('Success')
      })
      .catch(function (error) {
        $ons.notification.alert('Fail')
      });
    }
  },
  mounted: function () {
    this.$nextTick(function () {
      this.createChart()
    })
  }
};

const tempPage = {
  template: '#temp',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const busPage = {
  template: '#bus',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const mapPage = {
  template: '#map',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const libraryPage = {
  template: '#library',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const bookingPage = {
  template: '#booking',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const clinicPage = {
  template: '#clinic',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const lifestylePage = {
  template: '#lifestyle',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

const faultPage = {
  template: '#fault',
  props: ['toggleMenu', 'payMenu', 'title', 'titlefull'],
  data() {
    return {
    }
  },
  components: { customToolbar }
};

Vue.options.delimiters = ["[[", "]]"]

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
        Map: 'NTU Map',
        Lifestyle: 'Your Lifestyle',
        Library: 'Library Functions',
        Booking: 'Booking Facilities',
        Clinic: 'Clinic Services',
        Fault: 'Fault Reporting'
      },
      imgsrc: {
        Home: 'static/src/event.png',
        Food: 'static/src/food.png',
        Bus: 'static/src/bus.png',
        Lifestyle: 'static/src/bike.png',
        Library: 'static/src/library.png',
        Booking: 'static/src/booking.png',
        Clinic: 'static/src/clinic.png',
        Fault: 'static/src/faulty.png',
        Map: 'static/src/bus.png'
      },
      openSide: false
    };
  },
  components: {
    Home: homePage,
    Food: foodPage,
    Bus: busPage,
    Lifestyle: lifestylePage,
    Library: libraryPage,
    Booking: bookingPage,
    Clinic: clinicPage,
    Fault: faultPage,
    Map: mapPage
  }
});

/**/