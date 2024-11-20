import cv2
import numpy as np

# Cargar imagen binarizada (asegúrate de que esté en blanco y negro)
# Por ejemplo, generamos una imagen binarizada con una figura blanca sobre fondo negro
# Reemplaza 'binary_image.png' con la ruta de tu imagen binarizada
binary_image = cv2.imread('Imagenes/resultado_varios_rangos.jpg', cv2.IMREAD_GRAYSCALE)

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

# Mostrar resultados
print(f"Perímetro del contorno: {perimeter} píxeles")

# Visualizar la imagen del contorno
cv2.imshow("Contorno", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
