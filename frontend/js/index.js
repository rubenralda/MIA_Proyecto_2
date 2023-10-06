const lineNumbers = document.querySelector('.line-numbers')
const codigo = document.getElementById('textComandos');//textarea
const lineNumbersConsole = document.querySelector('.line-numbers-consola')
const consola = document.getElementById('textSalida');//textarea
const inputFile = document.createElement('input');
inputFile.type = 'file';
inputFile.accept = '.adsj';
inputFile.style.display = 'none';
document.body.appendChild(inputFile);

document.addEventListener("DOMContentLoaded", (e) => {
    e.preventDefault;
    if (localStorage.getItem("texto") != null) {
        codigo.value = localStorage.getItem("texto")
        let dispararEvento = new Event("keyup")
        codigo.dispatchEvent(dispararEvento)
    }
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