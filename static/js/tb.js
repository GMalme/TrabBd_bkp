function laj() {
    document.querySelectorAll('ajx').forEach(link => {
        const conteudo = document.getElementById('conteudo')
        console.log(link.href)
        link.addEventListener('click', function (e) {
            console.log(e.target.dataset.value)
            e.preventDefault()
            if (e.target.dataset.value != undefined)
            fetch("http://localhost:5000/load/" + e.target.dataset.value)
                .then(async (resp) => {
                console.log(await resp)
                document.getElementById('boxcontainer').innerHTML=await resp.text()
                })
        })
    })
}
function find(){
    document.querySelectorAll('a')[4].dataset.value
}
