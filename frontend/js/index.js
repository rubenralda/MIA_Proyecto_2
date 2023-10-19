const lineNumbers = document.querySelector('.line-numbers')
const codigo = document.getElementById('textComandos');//textarea
const lineNumbersConsole = document.querySelector('.line-numbers-consola')
const consola = document.getElementById('textSalida');//textarea
const inputFile = document.createElement('input');
const btnAbrir = document.getElementById("abrirArchivo");
const btnEjecutar = document.getElementById('btnEjecutar')
const btnReportes = document.getElementById('btnReportes')
const btnLogin = document.getElementById('btnLogin')
const btnCerrar = document.getElementById('btnCerrar')

inputFile.type = 'file';
inputFile.accept = '.adsj';
inputFile.style.display = 'none';
document.body.appendChild(inputFile);
url = 'http://18.225.248.23:80'

document.addEventListener("DOMContentLoaded", (e) => {
    e.preventDefault;
    if (localStorage.getItem("texto") != null) {
        codigo.value = localStorage.getItem("texto")
        let dispararEvento = new Event("keyup")
        codigo.dispatchEvent(dispararEvento)
    }
    if (localStorage.getItem("salida") != null) {
        consola.value = localStorage.getItem("salida")
        let dispararEvento = new Event("keyup")
        consola.dispatchEvent(dispararEvento)
    }
    fetch(url + "/login", {
        method : 'GET',
        headers : {
            'Content-Type': 'application/json'
        }
    })
    .then((res) => res.json())
    .then((res) => {
        console.log(res)
        if (res.usuario == null) {
            btnCerrar.style.display = "none";
        } else {
            btnLogin.style.display = "none";
        }
    })
    e.stopPropagation;
});

codigo.addEventListener("input", (e) =>{
    e.preventDefault;
    localStorage.setItem("texto", codigo.value)
    e.stopPropagation;
});

codigo.addEventListener("keyup", event => {
    const numberOfLines = event.target.value.split("\n").length;
    lineNumbers.innerHTML = Array(numberOfLines)
    .fill('<span></span>')
    .join('')
});

codigo.addEventListener("keydown", function(event) {
    if (event.key === "Tab") {
      event.preventDefault();  // Evita que el foco cambie al siguiente elemento
      const tabCharacter = "    "; // 4 espacios para simular un tabulador
      const start = this.selectionStart;
      const end = this.selectionEnd;
      this.value = this.value.substring(0, start) + tabCharacter + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + tabCharacter.length;
    }
});

consola.addEventListener("keyup", event => {
    const numberOfLines = event.target.value.split("\n").length;
    lineNumbersConsole.innerHTML = Array(numberOfLines)
    .fill('<span></span>')
    .join('')
});

inputFile.addEventListener('change', () => {
    const file = inputFile.files[0];
    console.log(file.path)
    console.log(file.webkitRelativePath )
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
      const fileContent = reader.result;
      codigo.value = fileContent
      localStorage.setItem("texto", fileContent)
      let dispararEvento = new Event("keyup")
      codigo.dispatchEvent(dispararEvento)
    };
});

btnAbrir.addEventListener("click", (e) =>{
    e.preventDefault();
    inputFile.click();
    e.stopPropagation();
});

btnEjecutar.addEventListener("click", async () => {
    comandos = localStorage.getItem("texto")
    if (comandos == null) {
        alert("Carga un archivo primero")
        return
    }
    localStorage.setItem("salida", "")
    for (const linea of comandos.split("\n")) {
        console.log(linea)
        if (linea.includes("pause")) {
            alert("Pausado")
            continue
        }
        await fetch(url + "/ejecutar", {
            method : 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({comando: linea})
        })
        .then((res) => res.json())
        .then((res) => {
            localStorage.setItem("salida", localStorage.getItem("salida") + res.mensaje)
        })
    }
    consola.value = localStorage.getItem("salida")
});

btnLogin.addEventListener("click", () => {
    window.location = "login.html"
});

btnCerrar.addEventListener("click", () => {
    fetch(url + "/ejecutar", {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({comando: `logout`})
    })
    .then((res) => res.json())
    .then((res) => {
        alert(res.mensaje);
        location.reload();
    });
});

btnReportes.addEventListener("click", () => {
    window.location = "report.html"
});