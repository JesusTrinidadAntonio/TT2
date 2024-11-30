import cv2
import numpy as np
import json
import os
import subprocess

# Abrir el archivo y cargar el contenido JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)

if config_list:
    # Obtener la primera configuración desde el archivo JSON
    config = config_list[0]
    imagen_path = config["ruta"]  # Ruta de la imagen desde el JSON

    # Leer la imagen desde el archivo
    imagen = cv2.imread(imagen_path)

    if imagen is None:
        print("No se pudo cargar la imagen.")
    else:
        # Procesamiento de la imagen
        imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)
        imagen_mediana = cv2.medianBlur(imagen_suavizada, 5)
        imagen_bilateral = cv2.bilateralFilter(imagen_mediana, d=9, sigmaColor=75, sigmaSpace=75)
        imagen_hsv = cv2.cvtColor(imagen_bilateral, cv2.COLOR_BGR2HSV)

        # Ajustar saturación y brillo
        factor_saturacion = 0.8
        imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)
        factor_brillo = 0.9
        imagen_hsv[:, :, 2] = np.clip(imagen_hsv[:, :, 2] * factor_brillo, 0, 255)

        # Convertir de nuevo de HSV a BGR
        imagen_aplanada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

        # Crear la carpeta 'Imagenes' si no existe
        if not os.path.exists('Imagenes'):
            os.makedirs('Imagenes')

        # Guardar la imagen procesada
        ruta_imagen_aplanada = os.path.join('Imagenes', 'ImagenAplanada.jpg')
        cv2.imwrite(ruta_imagen_aplanada, imagen_aplanada)
        print(f"Imagen procesada guardada en: {ruta_imagen_aplanada}")
        #subprocess.run(["python", "Color.py"])



else:
    print("El archivo JSON está vacío o mal formado.")
