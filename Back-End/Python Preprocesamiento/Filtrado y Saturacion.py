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

imagen=cv2.imread(ruta_imagen)

for i in range(10):
    imagen_G = cv2.GaussianBlur(imagen, (5, 5), 0)
    imagen_MB = cv2.medianBlur(imagen_G, 5)
    imagen_B = cv2.bilateralFilter(imagen_MB, d=9, sigmaColor=75, sigmaSpace=75)

# Cargar y procesar la imagen (operaciones de filtrado y saturación)
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    sys.exit(1)

# Aplicar operaciones de filtrado (como ejemplo, aquí puedes aplicar filtros)
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
factor_saturacion = 1.5
imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)
imagen_saturada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

# Guardar la imagen saturada
# Obtener la ruta absoluta del directorio actual y combinarla con "Imagenes/ImagenSaturada.jpg"
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagen_saturada = os.path.join(ruta_base, 'Imagenes', 'ImagenSaturada.jpg')

cv2.imwrite(ruta_imagen_saturada, imagen_saturada)


os.chdir(os.path.dirname(__file__))
subprocess.run([
    "python", "Color.py",
    str(respuestas_colores), str(respuestas_tamano), str(ruta_imagen_saturada)
])

