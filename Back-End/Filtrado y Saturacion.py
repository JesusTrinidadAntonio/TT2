from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
import subprocess

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Obtener los datos del formulario
    respuestas_colores = int(request.form['colores'])  # Cantidad de rangos de colores
    respuestas_tamano = request.form['tamano']         # Tamaño del objeto
    imagen = request.files['imagen']                    # La imagen es enviada como un archivo

    # Guardar la imagen en un directorio específico
    if imagen:
        ruta_imagen = os.path.join('uploads', imagen.filename)
        imagen.save(ruta_imagen)
    else:
        return jsonify({'error': 'No se proporcionó una imagen.'}), 400

    # Verificar si la imagen se ha cargado correctamente
    imagen_cargada = cv2.imread(ruta_imagen)
    if imagen_cargada is None:
        return jsonify({'error': 'No se pudo cargar la imagen.'}), 400

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
        str(respuestas_colores), str(respuestas_tamano), str(ruta_imagen_aplanada)
    ])

    return jsonify({
        'mensaje': 'Imagen procesada y datos recibidos correctamente.',
        'ruta_imagen_aplanada': ruta_imagen_aplanada
    })

if __name__ == '__main__':
    # Asegurarse de que el directorio de 'uploads' y 'Imagenes' existan
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('Imagenes', exist_ok=True)
    app.run(debug=True)


