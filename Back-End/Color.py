import cv2
import numpy as np
import os
import json

# Abrir el archivo y cargar el contenido JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)

if config_list:
    # Obtener la primera configuración desde el archivo JSON
    config = config_list[0]
    respuestas_colores = config["color"] 

# Variables y listas para almacenar los rangos de color en formato HSV
rango_colores_hsv = []
contador = 0

# Cargar la imagen desde la ruta proporcionada
ruta_imagen = 'Imagenes/ImagenAplanada.jpg'
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    exit(1)
imagen = cv2.resize(imagen, (800, 800))  # Redimensionar la imagen principal

# Función para mostrar mensajes en la ventana de imagen
def mostrar_mensaje(imagen, mensaje, duracion=1000):
    imagen_mensaje = imagen.copy()
    cv2.putText(imagen_mensaje, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Selecciona los colores", imagen_mensaje)
    cv2.waitKey(duracion)

# Función para seleccionar múltiples colores
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
        
        # Si se alcanzó el número requerido de colores, guarda los colores y pasa a la siguiente función
        if contador >= respuestas_colores:
            guardar_rangos()  # Guardar los colores seleccionados en un archivo .txt
            mostrar_mensaje(imagen, "Colores seleccionados. Procediendo...", 50)
            cv2.setMouseCallback("Selecciona los colores", lambda *args: None)  # Desactiva el callback
            cerrar_ventana()  # Cierra la ventana después de seleccionar todos los colores

# Función para guardar los rangos múltiples en un archivo de texto
def guardar_rangos():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(ruta_base, "colores", "colores_seleccionados.txt")
    
    # Guardar los colores seleccionados en formato de texto
    with open(ruta_archivo, "w") as f:
        for color in rango_colores_hsv:
            f.write(f"HSV: {color}\n")
    print("Colores guardados en colores_seleccionados.txt")

# Función para cerrar la ventana de OpenCV
def cerrar_ventana():
    print("Todos los colores han sido seleccionados. Cerrando la ventana...")
    cv2.destroyAllWindows()

# Configuración inicial de la ventana y callback
cv2.namedWindow("Selecciona los colores", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Selecciona los colores", 1150, 660)
cv2.imshow("Selecciona los colores", imagen)
cv2.moveWindow('Selecciona los colores', 90, 350) 
cv2.setMouseCallback("Selecciona los colores", seleccionar_multiples_colores)  # Iniciar con la selección de múltiples colores

cv2.waitKey(0)  # Esperar hasta que el usuario termine de seleccionar los colores
