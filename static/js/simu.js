// document.getElementById('nuevo-proceso-form').addEventListener('submit', function(event) {
//     event.preventDefault(); 
//     const id = document.getElementById('id').value;
//     const nombre = document.getElementById('nombre').value;
//     const tamano = document.getElementById('tamano').value;
//     const idRecurso = document.getElementById('id-recurso').value;

//     alert(`Proceso agregado:\nID: ${id}\nNombre: ${nombre}\nTamaño: ${tamano} KB\nID de Recurso: ${idRecurso}`);
//     this.reset();
// });

console.log('Hola Mundo');

var acc = document.getElementsByClassName("accordion");
for (let i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;

        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}


function ejecutar() {
    fetch('/ejecutar_proceso', {
        method: 'POST'
    })
    .then(response => {
        if(response.ok) {
            console.log("Correcto");
        } else {
            console.error("Error");
        }
    })
    .then(data => {
        document.getElementById('resultado').innerText = data; // Muestra el resultado en la página
    })
    .catch(error => console.error("Error de red: ", error));
}

setInterval(ejecutar, 1000);
