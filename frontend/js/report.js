const btn = document.getElementsByName('btnreporte')
const listado = document.getElementById('direcciones')

url = 'http://18.225.248.23:80'

document.addEventListener("DOMContentLoaded", () => {
    fetch(url + "/reportes", {
        method : 'GET',
        headers : {
            'Content-Type': 'application/json'
        }
    })
    .then((res) => res.json())
    .then((res) => {
        for (const direccion of res.listado) {
            listado.innerHTML += `<button type="button" class="list-group-item list-group-item-action" name="btnreporte">${direccion}</button>`
        }
        btn.forEach(boton => {
            boton.addEventListener("click", () => {
                mostrarReporte(boton.textContent)
                //boton.classList.add("active")
            });
        })
    });
});

async function mostrarReporte(direct) {
    await fetch(url + "/descargarReporte", {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({ruta: direct})
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('No se pudo obtener el archivo');
        }
        return res.blob();
    })
    .then(blop => {
        url2 = URL.createObjectURL(blop);
        window.open(url2, "_blank");
        URL.revokeObjectURL(url2);
    })
    .catch(error => {
        console.error(error);
    });
}