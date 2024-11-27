import cv2
import numpy as np
import sys
import subprocess
import os

# Verificar y capturar argumentos de línea de comandos
if len(sys.argv) > 3:
    respuestas_colores = int(sys.argv[1])  # Cantidad de rangos de colores a seleccionar
    respuestas_tamano = sys.argv[2]        # Tamaño del objeto de referencia (no utilizado en este código)
    ruta_imagen = sys.argv[3]              # Ruta de la imagen a procesar
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Variables y listas para almacenar los rangos de color en formato HSV
rango_colores_hsv = []
contador = 0
hsv_min = None
hsv_max = None

# Cargar la imagen desde la ruta proporcionada
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    sys.exit(1)
imagen = cv2.resize(imagen, (800, 800))  # Redimensionar la imagen principal

# Función para mostrar mensajes en la ventana de imagen
def mostrar_mensaje(imagen, mensaje, duracion=1000):
    imagen_mensaje = imagen.copy()
    cv2.putText(imagen_mensaje, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Selecciona los colores", imagen_mensaje)
    cv2.waitKey(duracion)

def seleccionar_multiples_colores(event, x, y, flags, param):
    global contador, rango_colores_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        # Obtener el color en formato BGR de la posición seleccionada
        color_bgr = imagen[y, x]
        # Convertir el color a formato HSV
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # Guardar el color HSV seleccionado
        rango_colores_hsv.append(color_hsv.tolist())
        contador += 1
        print(f"Color {contador} guardado: {color_hsv}")
        mostrar_mensaje(imagen, f"Color {contador} guardado")
        
        # Si se alcanzó el número requerido de colores, pasa a la siguiente función
        if contador >= respuestas_colores:
            cv2.setMouseCallback("Selecciona los colores", seleccionar_color_con_variacion)
            mostrar_mensaje(imagen, "Colores seleccionados. Procediendo a guardar...", 2000)

# Función para seleccionar un rango con variación alrededor del color en HSV
def seleccionar_color_con_variacion(event, x, y, flags, param):
    global hsv_min, hsv_max
    if event == cv2.EVENT_LBUTTONDOWN:
        color_bgr = imagen[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        # Crear un rango mínimo y máximo alrededor del color seleccionado en HSV
        rango_variacion_h = 20  # Rango de variación para el canal H (Hue)
        rango_variacion_s = 40  # Rango de variación para el canal S (Saturation)
        rango_variacion_v = 40  # Rango de variación para el canal V (Value)

        hsv_min = np.clip([color_hsv[0] - rango_variacion_h, 
                           color_hsv[1] - rango_variacion_s, 
                           color_hsv[2] - rango_variacion_v], 0, 255)
        hsv_max = np.clip([color_hsv[0] + rango_variacion_h, 
                           color_hsv[1] + rango_variacion_s, 
                           color_hsv[2] + rango_variacion_v], 0, 255)

        print(f"Rango de color HSV con variación seleccionado: Min = {hsv_min}, Max = {hsv_max}")

        guardar_rangos()         # Guardar los rangos múltiples seleccionados
        guardar_rango_variado()   # Guardar el rango con variación
        cv2.destroyAllWindows()   # Cerrar todas las ventanas después de seleccionar el color

# Función para guardar los rangos múltiples en un archivo de texto
def guardar_rangos():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(ruta_base, "colores", "colores_seleccionados.txt")
    
    # Guardar los colores seleccionados en formato de texto
    with open(ruta_archivo, "w") as f:
        for color in rango_colores_hsv:
            f.write(f"HSV: {color}\n")
    print("Colores guardados en colores_seleccionados.txt")

# Función para guardar el rango con variación en un archivo de texto separado
def guardar_rango_variado():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(ruta_base, "colores", "rango.txt")
    with open(ruta_archivo, "w") as f:
        f.write(f"Min: {hsv_min.tolist()}, Max: {hsv_max.tolist()}\n")
    print("Rango con variación guardado en rango.txt")

    # Cambiar al directorio del archivo actual y ejecutar el siguiente script
    os.chdir(os.path.dirname(__file__))
    subprocess.run([
        "python", "Deteccion.py",
        str(ruta_imagen), str(respuestas_tamano)
    ])

# Configuración inicial de la ventana y callback
cv2.namedWindow("Selecciona los colores", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Selecciona los colores", 800, 800)
cv2.imshow("Selecciona los colores", imagen)
cv2.setMouseCallback("Selecciona los colores", seleccionar_multiples_colores)

cv2.waitKey(0)
cv2.destroyAllWindows()