import cv2 
import numpy as np

img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/ImagenFiltrada.jpg")
cv2.imshow('Original',img)

umbral_bajo = np.array([0,120,0])
umbral_alto = np.array([120,255,120])
mask_verde = cv2.inRange(img, umbral_bajo, umbral_alto)
cv2.imshow('Seleccion',mask_verde)
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/Seleccion.jpg', mask_verde)


cv2.waitKey(0)
cv2.destroyAllWindows()