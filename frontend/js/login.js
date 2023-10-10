const btnLogin = document.getElementById('btnLogin');
url = 'http://127.0.0.1:4000'

btnLogin.addEventListener("click", async () => {
    let idParticion = document.getElementById("idParticion").value
    let usuario = document.getElementById("usuario").value
    let password = document.getElementById("pass").value
    if (usuario.includes(" ")) {
        usuario = `"${usuario}"`
    }
    if (password.includes(" ")) {
        password = `"${password}"`
    }
    await fetch(url + "/ejecutar", {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({comando: `login -user=${usuario} -pass=${password} -id=${idParticion}`})
    })
    .then((res) => res.json())
    .then((res) => {
        alert(res.mensaje)
        window.location = "index.html"
    });
});