import cv2 
import numpy as np

# Cargar la imagen
img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/imagen_saturada.jpg")

# Convertir la imagen a HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rango para los marrones (entre rojos y amarillos)
umbral_bajo_marron = np.array([10, 50, 50])   # Ajusta los valores para tonos marrones claros y oscuros
umbral_alto_marron = np.array([30, 255, 255])

# Rango para los verdes claros (Hue en el rango de los verdes, pero con alto valor y saturación)
umbral_bajo_verde_claro = np.array([36, 100, 150])  # Más saturados y con mayor brillo
umbral_alto_verde_claro = np.array([85, 255, 255])  # Mantiene el rango de verde, pero excluye los oscuros

# Crear la máscara para los verdes claros
mask_verde_claro = cv2.inRange(img_hsv, umbral_bajo_verde_claro, umbral_alto_verde_claro)

# Crear la máscara para los marrones
mask_marron = cv2.inRange(img_hsv, umbral_bajo_marron, umbral_alto_marron)

# Combinar las máscaras (mantener marrones y verdes claros)
mask_total = cv2.bitwise_or(mask_marron, mask_verde_claro)

# Aplicar la máscara a la imagen original
resultado = cv2.bitwise_and(img, img, mask=mask_total)

# Crear ventanas con un tamaño personalizado
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original', 600, 400)

cv2.namedWindow('Resultado', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Resultado', 600, 400)

# Mostrar las imágenes original y resultante
cv2.imshow('Original', img)
cv2.imshow('Resultado', resultado)

# Guardar la imagen resultante
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/Seleccion.jpg', resultado)

cv2.waitKey(0)
cv2.destroyAllWindows()
