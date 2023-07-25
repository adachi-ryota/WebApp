// Vue.js
import { createApp } from 'vue'
Vue.options.delimiters = ['[[', ']]'];



const create = createApp({
    methods: {
        cretememo: function() {

        }
    }
})
create.mount('#create')

const memo = createApp({
    data() {
        return {
            memono: "memo1"
        }
    }
})
memo.mount('#app')