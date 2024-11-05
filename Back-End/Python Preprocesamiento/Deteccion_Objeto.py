import cv2
import numpy as np
import sys

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

# Leer el archivo `rango.txt` y obtener los valores Min y Max
try:
    with open("C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/rango.txt", "r") as f:
        line = f.readline().strip()
        if line:
            # Extraer los valores mínimos y máximos del archivo
            min_part = line.split("], Max: ")[0]
            max_part = line.split("], Max: ")[1]

            # Convertir el texto a arrays de NumPy y aplicar una tolerancia
            hsv_min = np.array([int(x) for x in min_part.split(": ")[1].strip()[1:-1].split(", ")])
            hsv_max = np.array([int(x) for x in max_part.strip()[1:-1].split(", ")])

            # Aplicar tolerancia
            tolerancia = np.array([5, 40, 50])  # Ajustar tolerancia para cada componente
            hsv_min = np.clip(hsv_min - tolerancia, 0, 255)
            hsv_max = np.clip(hsv_max + tolerancia, 0, 255)

except FileNotFoundError:
    print("El archivo rango.txt no se encontró.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al procesar el archivo de colores: {e}")
    sys.exit(1)

# Crear la máscara para el único rango de color
mask = cv2.inRange(img_hsv, hsv_min, hsv_max)

# Aplicar la máscara a la imagen original
resultado = cv2.bitwise_and(img, img, mask=mask)

# Mostrar los resultados
cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original", 800, 800)

cv2.namedWindow("Resultado", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Resultado", 800, 800)

cv2.imshow("Original", img)
cv2.imshow("Resultado", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
