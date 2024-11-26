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
            cv2.setMouseCallback("Selecciona los colores", seleccionar_color)  # Cambiar al callback de selección de color

# Función para guardar los rangos múltiples en un archivo de texto
def guardar_rangos():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(ruta_base, "colores", "colores_seleccionados.txt")
    
    # Guardar los colores seleccionados en formato de texto
    with open(ruta_archivo, "w") as f:
        for color in rango_colores_hsv:
            f.write(f"HSV: {color}\n")
    print("Colores guardados en colores_seleccionados.txt")

# Función para seleccionar un rango con variación alrededor del color en HSV
def seleccionar_color(event, x, y, flags, param):
    global hsv_min, hsv_max
    if event == cv2.EVENT_LBUTTONDOWN:
        # Obtener el color en el punto seleccionado
        color_bgr = imagen[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        # Crear un rango mínimo y máximo alrededor del color seleccionado en HSV
        rango_variacion_h = 30  # Aumenté el rango de variación para H
        rango_variacion_s = 60  # Aumenté el rango de variación para S
        rango_variacion_v = 60  # Aumenté el rango de variación para V

        hsv_min = np.clip([color_hsv[0] - rango_variacion_h, 
                           color_hsv[1] - rango_variacion_s, 
                           color_hsv[2] - rango_variacion_v], 0, 255)
        hsv_max = np.clip([color_hsv[0] + rango_variacion_h, 
                           color_hsv[1] + rango_variacion_s, 
                           color_hsv[2] + rango_variacion_v], 0, 255)

        print(f"Rango de color HSV con variación seleccionado: Min = {hsv_min}, Max = {hsv_max}")

        mostrar_mensaje(imagen, "Color y rango seleccionados. Procediendo a la detección de la figura...", 1000)

        # Cambiar el callback a la función de detección de figuras
        cv2.setMouseCallback("Selecciona los colores", detectar_figura)

# Función para detectar la figura y aproximarla a un rectángulo o cuadrado
def detectar_figura(event, x, y, flags, param):
    global hsv_min, hsv_max
    if event == cv2.EVENT_LBUTTONDOWN:
        # Convertir la imagen a HSV
        img_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Crear una máscara para el rango HSV seleccionado
        mask = cv2.inRange(img_hsv, hsv_min, hsv_max)

        # Verificar si la máscara tiene píxeles blancos
        if np.sum(mask) == 0:
            print("No se detectaron píxeles dentro del rango HSV.")
            return

        # Aplicar la máscara para aislar el color seleccionado
        resultado = cv2.bitwise_and(imagen, imagen, mask=mask)

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(resultado, cv2.COLOR_BGR2GRAY)
        
        # Encontrar contornos en la imagen
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crear una imagen en blanco para dibujar los contornos regularizados
        combinada = np.zeros_like(gray)

        # Dibujar los contornos y aproximarlos
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Umbral para descartar ruido
                # Aproximar el contorno a un polígono regular (rectángulo)
                epsilon = 0.04 * cv2.arcLength(contour, True)  # Aproximación de contornos
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Si la forma aproximada tiene 4 puntos, la tratamos como un rectángulo o cuadrado
                if len(approx) == 4:
                    # Obtener los puntos del rectángulo
                    x, y, w, h = cv2.boundingRect(approx)

                    # Ajustar el contorno a un cuadrado si la relación es casi 1:1
                    if 0.9 <= w / h <= 1.1:  # Si las proporciones son cercanas a 1:1, ajustarlo a un cuadrado
                        size = max(w, h)
                        x, y, w, h = x, y, size, size

                    # Dibujar el rectángulo o cuadrado en la imagen combinada
                    cv2.rectangle(combinada, (x, y), (x + w, y + h), 255, thickness=cv2.FILLED)

        # Guardar la imagen combinada
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_combinada = os.path.join(ruta_base, "Imagenes", "figura_combinada.jpg")
        cv2.imwrite(ruta_combinada, combinada)

        print(f"Figura combinada (bordes ajustados a rectángulos/cuadrados) guardada en {ruta_combinada}")

        # Cerrar ventanas antes de llamar al próximo programa
        cv2.destroyAllWindows()

        # Llamar al próximo programa
        subprocess.run([
            "python", "Deteccion.py",
            str(ruta_imagen), str(respuestas_tamano), str(ruta_combinada)
        ])

# Configuración inicial de la ventana y callback
cv2.namedWindow("Selecciona los colores", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Selecciona los colores", 800, 800)
cv2.imshow("Selecciona los colores", imagen)
cv2.setMouseCallback("Selecciona los colores", seleccionar_multiples_colores)  # Iniciar con la selección de múltiples colores

cv2.waitKey(0)
cv2.destroyAllWindows()
