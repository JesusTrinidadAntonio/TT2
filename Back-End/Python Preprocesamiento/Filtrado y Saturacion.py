import cv2
import numpy as np
import sys
import subprocess
import os

# Verificar que se reciben los argumentos
if len(sys.argv) > 3:
    respuestas_colores = int(sys.argv[1])  # Cantidad de rangos de colores a seleccionar
    respuestas_tamano = sys.argv[2]        # Tamaño del objeto de referencia (no utilizado en este código)
    ruta_imagen = sys.argv[3]              # Ruta de la imagen a procesar
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar la imagen desde la ruta proporcionada
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    sys.exit(1)


imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)
imagen_mediana = cv2.medianBlur(imagen_suavizada, 5)
imagen_bilateral = cv2.bilateralFilter(imagen_mediana, d=9, sigmaColor=75, sigmaSpace=75)
imagen_hsv = cv2.cvtColor(imagen_bilateral, cv2.COLOR_BGR2HSV)
factor_saturacion = 0.8  # Reduce saturación para unificar colores
imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)
factor_brillo = 0.9
imagen_hsv[:, :, 2] = np.clip(imagen_hsv[:, :, 2] * factor_brillo, 0, 255)
imagen_aplanada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

# Guardar la imagen procesada
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagen_aplanada = os.path.join(ruta_base, 'Imagenes', 'ImagenAplanada.jpg')

cv2.imwrite(ruta_imagen_aplanada, imagen_aplanada)

print(f"Imagen procesada guardada en {ruta_imagen_aplanada}")

# Cambiar al directorio del archivo actual y ejecutar el siguiente script
os.chdir(os.path.dirname(__file__))
subprocess.run([
    "python", "Color.py",
    str(respuestas_colores), str(respuestas_tamano), str(ruta_imagen_aplanada)
])
