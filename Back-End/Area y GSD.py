import cv2
import numpy as np
import json
import os
import sqlite3
import shutil
from datetime import datetime 

# Cargar datos del archivo JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)

if config_list:
    config = config_list[0]
    config1 = config_list[1]

    # Valores extraídos del JSON
    image_width_px = int(config["imagen_tamano"])
    imagen_path = config["ruta"]
    pixel_size = float(config1["pixel_tam"])
    pixel_large = float(config1["pixel_tam_cuadrado"])

else:
    print("El archivo JSON está vacío o mal formado.")

# Leer la imagen

binary_image = cv2.imread('Imagenes/binarizada.jpg', cv2.IMREAD_GRAYSCALE)
imagen = cv2.imread('Imagenes/binarizada.jpg')

_, imagen_binaria = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)

# Detectar los contornos en la imagen binarizada
contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Calcular el perímetro total de los contornos
perimetro_total = 0
for contorno in contornos:
    perimetro_total += cv2.arcLength(contorno, True)

perimeter_m = perimetro_total * pixel_large

# Contar los píxeles blancos y calcular el área total
white_pixels_count = np.sum(binary_image == 255)
total_area_m2 = white_pixels_count * pixel_size

# Crear la ventana con OpenCV
panel_width = 250  # Ancho del panel lateral con los botones
img_height, img_width = imagen.shape[:2]
panel = np.ones((img_height, panel_width, 3), dtype=np.uint8) * 200  # Fondo gris claro

# Función para dibujar los botones y resultados en el panel
def draw_buttons(panel, perimeter_m, total_area_m2):
    # Texto de los resultados
    cv2.putText(panel, f"Perimeter: {perimeter_m:.2f} m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(panel, f"Area: {total_area_m2:.2f} m2", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Botones para registrar y descartar
    button_height = 60  # Alto de los botones
    cv2.rectangle(panel, (10, 120), (240, 120 + button_height), (180, 180, 180), -1)  # Registrar
    cv2.putText(panel, "Registrar Resultado", (15, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    cv2.rectangle(panel, (10, 200), (240, 200 + button_height), (180, 180, 180), -1)  # Descartar
    cv2.putText(panel, "Descartar Resultado", (15, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

# Función para almacenar el resultado en la base de datos y limpiar las carpetas
def store_results(perimeter_m, total_area_m2, fecha):
    # Conectar a la base de datos db_b049
    #conn = sqlite3.connect('db_b049.db')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    #cursor = conn.cursor()
#
    ## Insertar los resultados en la tabla cuerpo_a
    #cursor.execute(''' 
    #    INSERT INTO cuerpo_agua (nombre_cuerpo_a, fecha_cuerpo_a, area_cuerpo_a, perimetro_cuerpo_a, publicado_cuerpo_a, pendpub_cuerpo_a, id_dir_fk, id_imagen_fk, id_usuario_fk)
    #    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    #''', (fecha, total_area_m2, perimeter_m,))
#
    ## Guardar los cambios y cerrar la conexión
    #conn.commit()
    #conn.close()
    # Limpiar las carpetas "Imagenes" y "colores"
    shutil.rmtree('Imagenes')
    shutil.rmtree('colores')

    # Crear nuevamente las carpetas vacías
    os.makedirs('Imagenes', exist_ok=True)
    os.makedirs('colores', exist_ok=True)

    print("Resultado almacenado y carpetas limpiadas.")
    cv2.destroyAllWindows()

# Función para dibujar un mensaje de alerta
def show_alert_message(panel, message, color):
    alert_rect = (10, 300, 240, 60)  # Posición y tamaño del rectángulo de alerta
    cv2.rectangle(panel, (alert_rect[0], alert_rect[1]), (alert_rect[0] + alert_rect[2], alert_rect[1] + alert_rect[3]), color, -1)
    cv2.putText(panel, message, (15, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# Función para manejar los clics en los botones
def handle_button_click(x, y):
    if 10 <= x <= 240:
        if 120 <= y <= 180:
            print("Registrar resultado")
            fecha=datetime.now().strftime('%Y-%m-%d')
            store_results(perimeter_m,total_area_m2, fecha)
            show_alert_message(panel, "Resultado registrado.", (0, 255, 0))  # Mostrar mensaje verde
            cv2.destroyAllWindows()     # Cerrar la ventana después del mensaje
        elif 200 <= y <= 260:
            print("Descartar resultado")
            # Limpiar las carpetas "Imagenes" y "colores"
            shutil.rmtree('Imagenes')
            shutil.rmtree('colores')

            # Crear nuevamente las carpetas vacías
            os.makedirs('Imagenes', exist_ok=True)
            os.makedirs('colores', exist_ok=True)

            show_alert_message(panel, "Resultado descartado.", (0, 0, 255))  # Mostrar mensaje rojo
            cv2.destroyAllWindows()  # Cerrar la ventana después del mensaje

# Mostrar la imagen con el panel de botones
cv2.imshow("Resultados", imagen)

# Dibujar los botones y resultados en el panel
draw_buttons(panel, perimeter_m, total_area_m2)

# Combinar la imagen con el panel lateral
combined_image = np.hstack((panel, imagen))

# Función para capturar el clic y manejar las interacciones
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        handle_button_click(x, y)

# Asignar la función de callback al evento de clic
cv2.setMouseCallback("Resultados", mouse_callback)

# Mostrar la imagen combinada
while True:
    cv2.imshow("Resultados", combined_image)

    # Esperar la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar la ventana
cv2.destroyAllWindows()
