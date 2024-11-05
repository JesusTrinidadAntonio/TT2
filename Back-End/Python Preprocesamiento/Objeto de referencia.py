import cv2
import numpy as np
import sys
import subprocess

# Verificar y capturar argumentos de línea de comandos
if len(sys.argv) > 3:
    respuestas_tamano = sys.argv[2]  # Tamaño del objeto de referencia (no utilizado en este código)
    ruta_imagen = sys.argv[3]        # Ruta de la imagen a procesar
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Variables para almacenar el rango de color en HSV
hsv_min = None
hsv_max = None

# Función para manejar clics del mouse
def seleccionar_color(event, x, y, flags, param):
    global hsv_min, hsv_max
    if event == cv2.EVENT_LBUTTONDOWN:
        color_bgr = imagen[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        # Crear un pequeño rango alrededor del color seleccionado en HSV
        rango_variacion = 10  # Ajustar el rango según necesites
        hsv_min = np.clip(color_hsv - rango_variacion, 0, 255)
        hsv_max = np.clip(color_hsv + rango_variacion, 0, 255)

        print(f"Rango de color HSV seleccionado: Min = {hsv_min}, Max = {hsv_max}")

        # Guardar el rango en el archivo y cerrar la ventana
        guardar_rango()
        cv2.destroyAllWindows()  # Cierra todas las ventanas inmediatamente después de seleccionar el color

# Función para guardar el rango en un archivo de texto
def guardar_rango():
    with open("C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/rango.txt", "w") as f:
        f.write(f"Min: {hsv_min.tolist()}, Max: {hsv_max.tolist()}\n")
    print("Rango guardado en rango.txt")
    subprocess.run([
        "python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Deteccion de color.py",
        str(ruta_imagen)
    ])

# Cargar la imagen desde la ruta proporcionada y configurar la ventana
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    sys.exit(1)

# Crear y redimensionar la ventana con el nombre correcto
cv2.namedWindow("Selecciona el color de referencia", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Selecciona el color de referencia", 800, 800)
cv2.imshow("Selecciona el color de referencia", imagen)
cv2.setMouseCallback("Selecciona el color de referencia", seleccionar_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
