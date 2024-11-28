import cv2
import numpy as np
import sys
import os
import json


# Verificar y capturar argumentos
if len(sys.argv) > 2:
    pixel_size = float(sys.argv[1])  # Convertir a número flotante
    ruta_mask_uno = sys.argv[2]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)


# Abrir el archivo y cargar el contenido JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)
# Asegúrate de que la lista no esté vacía
if config_list:
    # Extraer el primer diccionario de la lista
    config = config_list[0]

    # Convertir los valores a tipo float (o int) si es necesario
    sensor_width_mm = float(config["sensor"])  # Convertir a float si es necesario
    altitude_m = float(config["altitud"])     # Convertir a float
    focal_distance_mm = float(config["focal"])  # Convertir a float
    image_width_px = int(config["imagen_tamano"])  # Convertir a entero

    # Calcular el GSD
    GSD = (sensor_width_mm * altitude_m) / (image_width_px * focal_distance_mm)
else:
    print("El archivo JSON está vacío o mal formado.")


os.chdir(os.path.dirname(__file__))
binary_image = cv2.imread('Imagenes/binarizada.jpg', cv2.IMREAD_GRAYSCALE)

contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Crear una imagen para dibujar el contorno
contour_image = np.zeros_like(binary_image)

# Dibujar los contornos con un grosor de 1
cv2.drawContours(contour_image, contours, -1, (255), 1)

# Calcular el perímetro usando la distancia euclidiana entre puntos
perimeter = 0
for contour in contours:
    perimeter += cv2.arcLength(contour, closed=True)

perimeter_m = perimeter * GSD

white_pixels_count = np.sum(binary_image == 255)

# Calcular el área total en metros cuadrados
total_area_m2 = white_pixels_count * pixel_size

 # Crear un diccionario con los resultados
resultados = {
        'area_m2': total_area_m2,
        'perimetro_m': perimeter_m
    }

    # Guardar los resultados en un archivo JSON
resultados_json = {
        "resultados": resultados,
        "procesado": True  # Bandera para indicar que los resultados están listos
    }

    # Guardar los resultados en un archivo JSON (usamos 'resultados.json')
with open('resultados.json', 'w') as json_file:
        json.dump(resultados_json, json_file, indent=4)

print("Resultados calculados y almacenados correctamente.")

cv2.waitKey(0)
cv2.destroyAllWindows()
