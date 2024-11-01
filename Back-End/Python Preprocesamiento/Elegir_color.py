import cv2
import numpy as np
import sys

if len(sys.argv) > 3:
    respuestas_colores = int(sys.argv[1])
    respuestas_tamano = sys.argv[2]
    ruta_imagen = sys.argv[3]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar la imagen
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print("Error al cargar la imagen.")
    sys.exit(1)

# Lista para almacenar los rangos de color en formato HSV
rango_colores_hsv = []

# Variables globales para almacenar el color mínimo y máximo
hsv_min = None
hsv_max = None

# Contador de rangos de colores seleccionados
contador = 0

# Cargar la imagen
imagen = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/jaguey.jpg")  # Reemplaza con la ruta de tu imagen
if imagen is None:
    print("Error al cargar la imagen.")
    sys.exit(1)


def mostrar_mensaje(imagen, mensaje, duracion=1000):
    imagen_mensaje = imagen.copy()
    cv2.putText(imagen_mensaje, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Selecciona los colores", imagen_mensaje)
    cv2.waitKey(duracion)  # Mostrar el mensaje por un tiempo determinado


# Función para manejar clics del mouse
def seleccionar_color(event, x, y, flags, param):
    global hsv_min, hsv_max, contador, rango_colores_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        # Obtén el color en el punto seleccionado
        color_bgr = imagen[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        if hsv_min is None:
            hsv_min = color_hsv  # Guarda el color mínimo
            print(f"Color mínimo seleccionado: {hsv_min}")
        elif hsv_max is None:
            hsv_max = color_hsv  # Guarda el color máximo
            print(f"Color máximo seleccionado: {hsv_max}")
            # Agrega el rango seleccionado a la lista
            rango_colores_hsv.append((hsv_min, hsv_max))
            contador += 1

            # Mostrar mensaje en la ventana de imagen
            mostrar_mensaje(imagen, f"Rango {contador} guardado")

            # Reinicia las variables para el siguiente rango
            hsv_min, hsv_max = None, None

        if contador >= respuestas_colores:
            print("Se han seleccionado todos los rangos de colores necesarios.")
            cv2.destroyAllWindows()

# Configura la ventana y la función de clic
cv2.namedWindow("Selecciona los colores")
cv2.setMouseCallback("Selecciona los colores", seleccionar_color)

# Muestra la imagen y espera las selecciones
while contador < respuestas_colores:
    cv2.imshow("Selecciona los colores", imagen)
    if cv2.waitKey(1) & 0xFF == 27:  # Presiona 'Esc' para salir
        break

cv2.destroyAllWindows()
