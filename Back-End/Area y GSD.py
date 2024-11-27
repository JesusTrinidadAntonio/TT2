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



with open('config.json', 'r') as file:
    config = json.load(file)

# Extraer variables del JSON
sensor_width_mm = config["sensor_width_mm"]
image_width_px = config["image_width_px"]
altitude_m = config["altitude_m"]
focal_distance_mm= config["focal_distance_mm"]

GSD = (sensor_width_mm*altitude_m)/(image_width_px*focal_distance_mm)

os.chdir(os.path.dirname(__file__))
binary_image = cv2.imread('Imagenes/binarizada.jpg', cv2.IMREAD_GRAYSCALE)
#ruta_mascara  = os.path.join(ruta_base, "colores", "mascara_varios_rangos.npy")
#binary_image = np.load(ruta_mascara)

# Detectar los contornos en la imagen
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

print(f"El área de los píxeles blancos es: {total_area_m2:.2f} metros cuadrados")
print(f"Perímetro del contorno: {perimeter_m:.2f} metros")


cv2.waitKey(0)
cv2.destroyAllWindows()


