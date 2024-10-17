import cv2 
import numpy as np

img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/ImagenFiltrada.jpg")

umbral_bajo = np.array([0,120,0])
umbral_alto = np.array([120,255,120])
mask_verde = cv2.inRange(img, umbral_bajo, umbral_alto)

# Crear ventanas con un tamaño personalizado
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original', 600, 400)  # Cambia las dimensiones a tu gusto

cv2.namedWindow('Resultado', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Resultado', 600, 400)

cv2.imshow('Original',img)
cv2.imshow('Resultado',mask_verde)
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/Seleccion.jpg', mask_verde)


cv2.waitKey(0)
cv2.destroyAllWindows()