import cv2
import numpy as np
import sys
import os
import subprocess

# Verificar y capturar argumentos
if len(sys.argv) > 2:
    respuesta_tamano = float(sys.argv[1])  # Convertir a número flotante
    ruta_mask_uno = sys.argv[2]

else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar la máscara desde el archivo
try:
    mask_uno = np.load(ruta_mask_uno)
except Exception as e:
    print(f"Error al cargar la máscara desde {ruta_mask_uno}: {e}")
    sys.exit(1)

# Validar que la máscara tiene valores binarios
if not np.all(np.isin(mask_uno, [0, 255])):
    print("La máscara cargada no es binaria (debe contener solo valores 0 y 255).")
    sys.exit(1)

# Contar los píxeles blancos (255)
white_pixels_count = np.sum(mask_uno == 255)

if white_pixels_count == 0:
    print("No hay píxeles blancos en la máscara. No se puede calcular el tamaño del pixel.")
    sys.exit(1)

# Calcular el tamaño de cada píxel
pixel_size = respuesta_tamano / white_pixels_count


os.chdir(os.path.dirname(__file__))
subprocess.run(["python", "Area y GSD.py", str(pixel_size), str(ruta_mask_uno)])

