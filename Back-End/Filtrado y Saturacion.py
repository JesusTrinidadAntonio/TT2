import cv2
import numpy as np
import json

# Abrir el archivo y cargar el contenido JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)
# Asegúrate de que la lista no esté vacía
if config_list:
    # Extraer el primer diccionario de la lista
    config = config_list[0]

    # Convertir los valores a tipo float (o int) si es necesario
    imagen = float(config["sensor"])  # Convertir a float si es necesario

else:
    print("El archivo JSON está vacío o mal formado.")

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
