import cv2
import numpy as np
import sys
import subprocess

# Verificar que se reciben los argumentos
if len(sys.argv) > 1:
    ruta_imagen = sys.argv[1]
else:
    print("No se proporcionaron argumentos.")
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
ruta_imagen_saturada = 'C:/Users/jesus/Documents/TT2/Imagenes/ImagenSaturada.jpg'
cv2.imwrite(ruta_imagen_saturada, imagen_saturada)

# Llamar a Detencion de color.py con la imagen saturada y los rangos HSV
subprocess.run(["python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Deteccion de color.py", ruta_imagen])
