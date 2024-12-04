document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir que el formulario se envíe de la forma tradicional

    // Obtener los datos del formulario y convertirlos a números flotantes
    const colores = document.getElementById('colores').value;
    const tamano = document.getElementById('tamano').value;
    const imagen = document.getElementById('imagen').files[0]; // Obtener el archivo seleccionado

    // Validación de campos
    if (!colores || !tamano || !imagen) {
        alert("Por favor llena todos los campos.");
        return;
    }



    // Crear un objeto FormData para enviar los datos y la imagen
    const formData = new FormData();
    formData.append('colores', colores);
    formData.append('tamano', tamano);
    formData.append('imagen', imagen);

    // Enviar los datos al servidor utilizando fetch
    fetch('http://127.0.0.1:5000/submit_form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Formulario enviado con éxito');
        } else {
            alert('Hubo un problema con el formulario');
        }
    });
});
