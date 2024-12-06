import cv2
import numpy as np
import json
import os
import shutil
from datetime import datetime

# Cargar datos del archivo JSON
try:
    with open('datos.json', 'r') as file:
        config_list = json.load(file)
    if config_list:
        config = config_list[0]
        config1 = config_list[1]
        # Valores extraídos del JSON
        image_width_px = int(config["imagen_tamano"])
        imagen_path = config["ruta"]
        pixel_size = float(config1["pixel_tam"])
        pixel_large = float(config1["pixel_tam_cuadrado"])
    else:
        print("El archivo 'datos.json' está vacío o mal formado.")
        exit(1)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error al leer el archivo 'datos.json': {e}")
    exit(1)

# Verificar si el archivo de imagen existe
if not os.path.exists('Imagenes/binarizada.jpg'):
    print("La imagen 'Imagenes/binarizada.jpg' no existe.")
    exit(1)

# Leer la imagen
binary_image = cv2.imread('Imagenes/binarizada.jpg', cv2.IMREAD_GRAYSCALE)
imagen = cv2.imread('Imagenes/binarizada.jpg')

# Binarizar la imagen (umbral de 127)
_, imagen_binaria = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)

# Detectar los contornos en la imagen binarizada
contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Calcular el perímetro total de los contornos
perimetro_total = 0
for contorno in contornos:
    perimetro_total += cv2.arcLength(contorno, True)

perimeter_m = perimetro_total * pixel_large

# Contar los píxeles blancos y calcular el área total
white_pixels_count = np.sum(binary_image == 255)
total_area_m2 = white_pixels_count * pixel_size

# Función para almacenar el resultado en el archivo JSON y limpiar las carpetas
def store_results(perimeter_m, total_area_m2, fecha):

    resultados = {
        'area': total_area_m2,
        'perimetro': perimeter_m,
        'fecha': fecha,
    }

    # Intentar leer el archivo resultados.json y cargar los datos existentes
    try:
        with open('resultados.json', 'r') as file:
            data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Si el archivo no existe o está mal formado, inicializamos con lista vacía

    # Agregar los nuevos resultados
    data.append(resultados)

    # Guardar los datos actualizados en el archivo resultados.json
    try:
        with open('resultados.json', 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error al guardar los resultados en 'resultados.json': {e}")
        return

   # # Limpiar las carpetas "Imagenes" y "colores"
   # if os.path.exists('Imagenes'):
   #     shutil.rmtree('Imagenes')
   # if os.path.exists('colores'):
   #     shutil.rmtree('colores')
#
   # # Crear nuevamente las carpetas vacías
   # os.makedirs('Imagenes', exist_ok=True)
   # os.makedirs('colores', exist_ok=True)

    print("Resultado almacenado y carpetas limpiadas.")

# Ejecutar la función de almacenar resultados
fecha = datetime.now().strftime('%Y-%m-%d')
store_results(perimeter_m, total_area_m2, fecha)
