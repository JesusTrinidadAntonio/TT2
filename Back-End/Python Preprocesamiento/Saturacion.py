import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('C:/Users/jesus/Documents/TT2/Imagenes/ImagenFiltrada.jpg')

# Convertir la imagen de BGR a HSV
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Multiplicar el canal de saturación por un factor para aumentarlo
factor_saturacion = 1.5  # Puedes ajustar este valor
imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)

# Convertir la imagen de vuelta a BGR
imagen_saturada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

# Mostrar la imagen original y la saturada
cv2.imshow('Imagen Original', imagen)
cv2.imshow('Imagen con Saturacion', imagen_saturada)

# Esperar a que se cierre la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()

# Guardar la imagen saturada si deseas
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/imagen_saturada.jpg', imagen_saturada)
