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
        'sensor': sensor,
        'altitud': altitud,
        'focal': focal,
        'imagen_tamano': ancho  # Solo el ancho de la imagen
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


    # Procesamiento de la imagen
    imagen_suavizada = cv2.GaussianBlur(imagen_cargada, (5, 5), 0)
    imagen_mediana = cv2.medianBlur(imagen_suavizada, 5)
    imagen_bilateral = cv2.bilateralFilter(imagen_mediana, d=9, sigmaColor=75, sigmaSpace=75)
    imagen_hsv = cv2.cvtColor(imagen_bilateral, cv2.COLOR_BGR2HSV)

    # Ajustar saturación y brillo
    factor_saturacion = 0.8
    imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)
    factor_brillo = 0.9
    imagen_hsv[:, :, 2] = np.clip(imagen_hsv[:, :, 2] * factor_brillo, 0, 255)

    imagen_aplanada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

    # Guardar la imagen procesada
    ruta_imagen_aplanada = os.path.join('Imagenes', 'ImagenAplanada.jpg')
    cv2.imwrite(ruta_imagen_aplanada, imagen_aplanada)

    # Cambiar al directorio del archivo actual y ejecutar el siguiente script
    os.chdir(os.path.dirname(__file__))
    subprocess.run([
     "python", "Color.py",
     str(respuestas_colores),str(respuestas_tamano),str(ruta_imagen_aplanada)
    ])

    while True:
        time.sleep(1)  # Esperar un segundo antes de volver a verificar
        if os.path.exists('resultados.json'):
            with open('resultados.json', 'r') as json_file:
                data = json.load(json_file)
                if data.get('procesado', False):
                    # Los resultados están listos, retornamos los datos a resultado.html
                    return render_template("resultado.html", resultados=data['resultados'])

    # Si no se encuentran resultados después de un tiempo (puedes agregar un límite de tiempo)
    return "Error: Los resultados no están disponibles aún.", 500

if __name__ == '__main__':
    # Asegurarse de que el directorio de 'uploads' y 'Imagenes' existan
    #os.makedirs('uploads', exist_ok=True)
    os.makedirs('Imagenes', exist_ok=True)
    app.run(debug=True)