document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir que el formulario se envíe de la forma tradicional

    // Obtener los datos del formulario y convertirlos a números flotantes
    const colores = document.getElementById('colores').value;
    const tamano = document.getElementById('tamano').value;
    const sensor = parseFloat(document.getElementById('sensor').value);
    const altitud = parseFloat(document.getElementById('altitud').value);
    const focal = parseFloat(document.getElementById('focal').value);
    const imagen = document.getElementById('imagen').files[0]; // Obtener el archivo seleccionado

    // Validación de campos
    if (!colores || !tamano || !sensor || !altitud || !focal || !imagen) {
        alert("Por favor llena todos los campos.");
        return;
    }

    // Verificar si los valores de sensor, altitud y focal son números válidos
    if (isNaN(sensor) || isNaN(altitud) || isNaN(focal)) {
        alert("Por favor ingrese valores válidos para el sensor, altitud y distancia focal.");
        return; // Detener la ejecución si algún valor no es válido
    }

    // Crear un objeto FormData para enviar los datos y la imagen
    const formData = new FormData();
    formData.append('colores', colores);
    formData.append('tamano', tamano);
    formData.append('sensor', sensor);
    formData.append('altitud', altitud);
    formData.append('focal', focal);
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
