import cv2
import numpy as np
import sys
import json
import math

# Abrir el archivo y cargar el contenido JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)

if config_list:
    # Obtener la primera configuración desde el archivo JSON
    config = config_list[0]
    respuesta_tamano = float(config["tamano"])
    #respuesta_tamano_lado = float(config["tamano_lado"])

ruta_imagen = 'Imagenes/figura_combinada.jpg'

# Cargar la imagen combinada
try:
    imagen_combinada = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)  # Cargar imagen en escala de grises
    if imagen_combinada is None:
        print(f"No se pudo cargar la imagen desde {ruta_imagen}.")
        sys.exit(1)
except Exception as e:
    print(f"Error al cargar la imagen desde {ruta_imagen}: {e}")
    sys.exit(1)

# Binarizar la imagen para asegurar que tenga solo valores 0 y 255
_, imagen_binarizada = cv2.threshold(imagen_combinada, 127, 255, cv2.THRESH_BINARY)

# Validar que la imagen contiene valores binarios
if not np.all(np.isin(imagen_binarizada, [0, 255])):
    print("La imagen binarizada aún no es completamente binaria (debe contener solo valores 0 y 255).")
    sys.exit(1)

# Contar los píxeles blancos (valor 255)
white_pixels_count = np.sum(imagen_binarizada == 255)

if white_pixels_count == 0:
    print("No hay píxeles blancos en la imagen. No se puede calcular el tamaño del píxel.")
    sys.exit(1)

# Calcular el tamaño de cada píxel
pixel_size = respuesta_tamano / white_pixels_count


contornos, _ = cv2.findContours(imagen_binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contorno_cuadrado = contornos[0]

p1, p2 = contorno_cuadrado[0][0], contorno_cuadrado[1][0]
lado_cuadrado_pixeles = int(np.linalg.norm(p1 - p2))

# Calcular el tamaño del píxel con el lado del cuadrado
if lado_cuadrado_pixeles == 0:
    print("El lado del cuadrado tiene 0 píxeles. No se puede calcular el tamaño del píxel.")
    sys.exit(1)

# Calcular el tamaño de cada píxel con el lado del cuadrado
pixel_size_cuadrado = math.sqrt(respuesta_tamano) / lado_cuadrado_pixeles

pixel = {
    'pixel_tam': pixel_size,
    'pixel_tam_cuadrado': pixel_size_cuadrado
}

try:
    with open('datos.json', 'r') as file:
        data = json.load(file)  # Cargar los datos existentes
except (FileNotFoundError, json.JSONDecodeError):
    data = []  # Si no existe o si hay un error al leer, usamos una lista vacía

# Agregar los nuevos datos
data.append(pixel)

# Guardar los datos actualizados en el archivo JSON
with open('datos.json', 'w') as file:
    json.dump(data, file, indent=4)
