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

# Leer los colores desde el archivo
colores_hsv = []
try:
    with open("C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/rangos_colores.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Saltar líneas vacías
            # Extraer el color mínimo del rango
            try:
                min_part = line.split("], Max: ")[0]
                color_hsv = min_part.split(": ")[1].strip()[1:-1].split(", ")
                # Agregar el color como un array de NumPy
                colores_hsv.append(np.array([int(x) for x in color_hsv]))
            except (IndexError, ValueError) as e:
                print(f"Línea mal formateada: {line}. Error: {e}")
                continue  # Saltar la línea si hay un error

except FileNotFoundError:
    print("El archivo rangos_colores.txt no se encontró.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado al procesar el archivo de colores: {e}")
    sys.exit(1)

# Crear una máscara combinada para los colores
mask_total = None
for color in colores_hsv:
    # Definir un rango alrededor del color seleccionado (puedes ajustar la tolerancia)
    tolerancia = 10
    hsv_min = np.clip(color - tolerancia, 0, 255)
    hsv_max = np.clip(color + tolerancia, 0, 255)
    mask = cv2.inRange(img_hsv, hsv_min, hsv_max)
    mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

# Aplicar la máscara a la imagen original
resultado = cv2.bitwise_and(img, img, mask=mask_total)

# Mostrar y guardar la imagen resultante
cv2.imshow('Original', img)
cv2.imshow('Resultado', resultado)
cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/Seleccion.jpg', resultado)

cv2.waitKey(0)
cv2.destroyAllWindows()
