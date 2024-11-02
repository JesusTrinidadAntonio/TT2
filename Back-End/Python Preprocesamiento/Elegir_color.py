import cv2
import numpy as np
import sys
import subprocess

# Verificar y capturar argumentos de línea de comandos
if len(sys.argv) > 3:
    respuestas_colores = int(sys.argv[1])  # Cantidad de rangos de colores a seleccionar
    respuestas_tamano = sys.argv[2]        # Tamaño del objeto de referencia (no utilizado en este código)
    ruta_imagen = sys.argv[3]              # Ruta de la imagen a procesar
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Lista para almacenar los rangos de color en formato HSV
rango_colores_hsv = []
contador = 0

# Variables globales para almacenar el color mínimo y máximo
hsv_min = None
hsv_max = None

# Función para mostrar mensajes en la ventana de imagen
def mostrar_mensaje(imagen, mensaje, duracion=1000):
    imagen_mensaje = imagen.copy()
    cv2.putText(imagen_mensaje, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Selecciona los colores", imagen_mensaje)
    cv2.waitKey(duracion)

# Función para manejar clics del mouse
def seleccionar_color(event, x, y, flags, param):
    global hsv_min, hsv_max, contador, rango_colores_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        color_bgr = imagen[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        if hsv_min is None:
            hsv_min = color_hsv
            print(f"Color mínimo seleccionado: {hsv_min}")
        elif hsv_max is None:
            hsv_max = color_hsv
            rango_colores_hsv.append((hsv_min.tolist(), hsv_max.tolist()))
            print(f"Rango {contador + 1} guardado: Min = {hsv_min}, Max = {hsv_max}")
            contador += 1
            mostrar_mensaje(imagen, f"Rango {contador} guardado")
            hsv_min, hsv_max = None, None  # Reiniciar para el siguiente rango

        if contador >= respuestas_colores:
            cv2.destroyAllWindows()
            guardar_rangos()  # Llamar a la función para guardar los rangos

# Función para guardar los rangos en un archivo de texto
def guardar_rangos():
    with open("C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/rangos_colores.txt", "w") as f:
        for rango in rango_colores_hsv:
            min_hsv = rango[0]
            max_hsv = rango[1]
            f.write(f"Min: {min_hsv}, Max: {max_hsv}\n")
    
    print("Rangos guardados en rangos_colores.txt")
    subprocess.run(["python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Filtrado y Saturacion.py", ruta_imagen])
    
# Cargar la imagen desde la ruta proporcionada y configurar la ventana
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    sys.exit(1)

cv2.imshow("Selecciona los colores", imagen)
cv2.setMouseCallback("Selecciona los colores", seleccionar_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
