import cv2
import numpy as np
import json

with open('Pruebas/config.json', 'r') as file:
    config = json.load(file)

# Extraer variables del JSON
sensor_width_mm = config["sensor_width_mm"]
image_width_px = config["image_width_px"]
altitude_m = config["altitude_m"]
focal_distance_mm= config["focal_distance_mm"]

GSD = (sensor_width_mm*altitude_m)/(image_width_px*focal_distance_mm)

# Cargar la imagen binarizada
binary_image = cv2.imread('Pincel/Imagenes/pincel_masked.png', cv2.IMREAD_GRAYSCALE)

# Detectar los contornos en la imagen
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Crear una imagen para dibujar el contorno
contour_image = np.zeros_like(binary_image)

# Dibujar los contornos con un grosor de 1
cv2.drawContours(contour_image, contours, -1, (255), 1)

# Calcular el perímetro en píxeles y convertirlo a metros
perimeter_px = 0
for contour in contours:
    perimeter_px += cv2.arcLength(contour, closed=True)

# Convertir el perímetro a metros
perimeter_m = perimeter_px * GSD

# Mostrar resultados
print(f"Perímetro del contorno: {perimeter_px:.2f} píxeles")
print(f"Perímetro del contorno: {perimeter_m:.2f} metros")

# Visualizar la imagen del contorno
cv2.imshow("Contorno", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
