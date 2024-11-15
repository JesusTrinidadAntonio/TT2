import cv2
import numpy as np
import os

# Cargar la imagen desde la ubicación especificada
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(ruta_base, 'Imagenes', 'binarizada.jpg')

img = cv2.imread(ruta_imagen)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Leer la imagen en escala de grises
image = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# Verificar si la imagen se cargó correctamente
if image is None:
    print("Error: no se pudo cargar la imagen en", ruta_imagen)
    exit()

# Pedir al usuario el tamaño en metros cuadrados de un píxel
pixel_size_m2 = float(input("Introduce el tamaño en metros cuadrados de un píxel: "))

# Contar los píxeles blancos (valor 255)
white_pixels_count = np.sum(image == 255)

# Calcular el área total en metros cuadrados
total_area_m2 = white_pixels_count * pixel_size_m2

print(f"El área de los píxeles blancos es: {total_area_m2:.2f} metros cuadrados")
