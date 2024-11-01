import cv2
import numpy as np
import sys

# Captura los argumentos de línea de comandos
if len(sys.argv) > 2:
    respuestas_colores = sys.argv[1]
    respuestas_tamano = sys.argv[2]
else:
    print("No se proporcionaron argumentos suficientes.")
# Lista para almacenar los rangos mínimos y máximos de colores HSV
rango_colores_hsv = []

# Variables para almacenar el mínimo y máximo
hsv_min = None
hsv_max = None

# Número máximo de rangos de colores a seleccionar
num_rangos_a_seleccionar = respuestas_colores  # Puedes ajustar este número según tus necesidades

print("Colores del cuerpo de agua",num_rangos_a_seleccionar)
