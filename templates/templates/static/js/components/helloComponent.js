var helloComponent = Vue.component('hello-component', {
    props: ['message'],
    template: `
    <div>
        <h1>{{ message }}!</h1>
    </div>
    `
  })