from flask import Flask, request, jsonify, render_template 
from PIL import Image
import cv2
import numpy as np
import os
import subprocess
import json
import time

app = Flask(__name__)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Obtener los datos del formulario
    respuestas_colores = int(request.form['colores'])  # Cantidad de rangos de colores
    respuestas_tamano = request.form['tamano']         # Tamaño del objeto
    sensor = request.form['sensor']                     # Sensor
    altitud = request.form['altitud']                   # Altitud
    focal = request.form['focal']                       # Focal
    imagen = request.files['imagen']                    # La imagen recibida como archivo

        # Guardar la imagen en un directorio específico
    if imagen:
        ruta_imagen = os.path.join('imagenes', "Cuerpo_Agua.jpg")
        imagen.save(ruta_imagen)
    else:
        return jsonify({'error': 'No se proporcionó una imagen.'}), 400

    # Verificar si la imagen se ha cargado correctamente
    imagen_cargada = cv2.imread(ruta_imagen)
    if imagen_cargada is None:
        return jsonify({'error': 'No se pudo cargar la imagen.'}), 400
    

    try:
        img = Image.open(imagen)  # Usamos PIL para abrir la imagen
        ancho, alto = img.size  # Devuelve una tupla (ancho, alto)
    except Exception as e:
        return f"Error al abrir la imagen: {e}", 400

    # Mostrar el tamaño de la imagen
    print(f"Tamaño de la imagen: {ancho} x {alto} píxeles")

    # Datos a guardar (puedes incluir el tamaño de la imagen si lo deseas)
    new_data = {
        'color':respuestas_colores,
        'tamano': respuestas_tamano,
        'sensor': sensor,
        'altitud': altitud,
        'focal': focal,
        'imagen_tamano': ancho,  # Solo el ancho de la imagen
        'ruta': ruta_imagen
    }

    # Intentar leer el archivo JSON y cargar los datos existentes
    try:
        with open('datos.json', 'r') as file:
            data = []  # Leer datos existentes
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Si no existe o si hay un error al leer, usamos una lista vacía

    # Agregar los nuevos datos
    data.append(new_data)

    # Guardar los datos actualizados en el archivo JSON
    with open('datos.json', 'w') as file:
        json.dump(data, file, indent=4)


#   # Cambiar al directorio del archivo actual y ejecutar el siguiente script
#   os.chdir(os.path.dirname(__file__))
#   subprocess.run([
#    "python", "Filtrado y Saturacion.py",
#    str(ruta_imagen)
#   ])
#
#   while True:
#       time.sleep(1)  # Esperar un segundo antes de volver a verificar
#       if os.path.exists('resultados.json'):
#           with open('resultados.json', 'r') as json_file:
#               data = json.load(json_file)
#               if data.get('procesado', False):
#                   # Los resultados están listos, retornamos los datos a resultado.html
#                   return render_template("resultado.html", resultados=data['resultados'])
#
#   # Si no se encuentran resultados después de un tiempo (puedes agregar un límite de tiempo)
#   return "Error: Los resultados no están disponibles aún.", 500

if __name__ == '__main__':
    os.makedirs('Imagenes', exist_ok=True)
    app.run(debug=True)