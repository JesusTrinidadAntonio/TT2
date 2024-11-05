import cv2
import numpy as np
import sys
import subprocess

# Verificar y capturar argumentos
if len(sys.argv) > 1:
    ruta_imagen_saturada = sys.argv[1]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar la imagen saturada
img = cv2.imread(ruta_imagen_saturada)
if img is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen_saturada}")
    sys.exit(1)

# Convertir la imagen a HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
colores_hsv = []
try:
    with open("C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/rangos_colores.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Extraer los valores mínimos y máximos del archivo
            min_part = line.split("], Max: ")[0]
            max_part = line.split("], Max: ")[1]

            # Convertir el texto a arrays de NumPy y aplicar una tolerancia
            hsv_min = np.array([int(x) for x in min_part.split(": ")[1].strip()[1:-1].split(", ")])
            hsv_max = np.array([int(x) for x in max_part.strip()[1:-1].split(", ")])
            
            # Aplicar tolerancia
            tolerancia = np.array([10, 40, 50])  # Ajustar tolerancia para cada componente
            hsv_min = np.clip(hsv_min - tolerancia, 0, 255)
            hsv_max = np.clip(hsv_max + tolerancia, 0, 255)

            # Añadir al listado de colores con tolerancia
            colores_hsv.append((hsv_min, hsv_max))

except FileNotFoundError:
    print("El archivo rangos_colores.txt no se encontró.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al procesar el archivo de colores: {e}")
    sys.exit(1)

# Crear la máscara total combinando todos los rangos con tolerancia
mask_total = None
for hsv_min, hsv_max in colores_hsv:
    mask = cv2.inRange(img_hsv, hsv_min, hsv_max)
    mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

# Aplicar la máscara a la imagen original
resultado = cv2.bitwise_and(img, img, mask=mask_total)

# Mostrar los resultados
cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original", 800, 800)

cv2.namedWindow("Resultado", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Resultado", 800, 800)

cv2.imshow("Original", img)
cv2.imshow("Resultado", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()

subprocess.run([
    "python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Deteccion_Objeto.py",
    str(ruta_imagen_saturada)
])