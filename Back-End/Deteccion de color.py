import cv2 
import numpy as np

img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/ImagenFiltrada.jpg")

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rango para el color verde del lago
umbral_bajo_verde = np.array([35, 40, 40])   # Ajusta según el tono, saturación y valor
umbral_alto_verde = np.array([85, 255, 255]) # Ajusta según el tono, saturación y valor

# Rango para el color marrón del lago
umbral_bajo_marron = np.array([10, 100, 20])  # Ajusta según el tono, saturación y valor
umbral_alto_marron = np.array([20, 255, 200]) # Ajusta según el tono, saturación y valor

# Máscaras para los colores del lago
mask_verde = cv2.inRange(img_hsv, umbral_bajo_verde, umbral_alto_verde)
mask_marron = cv2.inRange(img_hsv, umbral_bajo_marron, umbral_alto_marron)

# Combinar ambas máscaras
mask_total = cv2.bitwise_or(mask_verde, mask_marron)

resultado = cv2.bitwise_and(img, img, mask=mask_total)

# Crear ventanas con un tamaño personalizado
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original', 600, 400)  # Cambia las dimensiones a tu gusto

cv2.namedWindow('Resultado', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Resultado', 600, 400)

cv2.imshow('Original',img)
cv2.imshow('Resultado',resultado)
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/Seleccion.jpg', resultado)


cv2.waitKey(0)
cv2.destroyAllWindows()