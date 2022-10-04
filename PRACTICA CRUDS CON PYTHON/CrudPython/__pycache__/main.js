const app=new Vue({
    el:"#app",
    data:{
        productos:[]
    },
    created() {
        var url='http://localhost:5000/productos'
        this.fetchData(url)
    },
    methods:{
        fetchData(url){
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.productos = data;
                   // this.loading = false;
                })
                .catch(err => {
                   // this.errored = true
                })
        }
    }
})

