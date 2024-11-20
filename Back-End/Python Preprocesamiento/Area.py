import cv2
import numpy as np

# Ruta de la imagen binarizada
image_path = "Pincel/Imagenes/Lagos1_bin.png"

# Leer la imagen en escala de grises
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Verificar si la imagen se cargó correctamente
if image is None:
    print("Error: no se pudo cargar la imagen en", image_path)
    exit()

# Pedir al usuario el tamaño en metros cuadrados de un píxel
pixel_size_m2 = float(input("Introduce el tamaño en metros cuadrados de un píxel: "))

# Contar los píxeles blancos (valor 255)
white_pixels_count = np.sum(image == 255)

# Calcular el área total en metros cuadrados
total_area_m2 = white_pixels_count * pixel_size_m2

print(f"El área de los píxeles blancos es: {total_area_m2:.2f} metros cuadrados")
