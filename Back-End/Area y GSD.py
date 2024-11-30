import cv2
import numpy as np
import json
import os
import sqlite3
import shutil

# Cargar datos del archivo JSON
with open('datos.json', 'r') as file:
    config_list = json.load(file)

if config_list:
    config = config_list[0]
    config1 = config_list[1]

    # Valores extraídos del JSON
    sensor_width_mm = float(config["sensor"])
    altitude_m = float(config["altitud"])
    focal_distance_mm = float(config["focal"])
    image_width_px = int(config["imagen_tamano"])
    imagen_path = config["ruta"]
    pixel_size = float(config1["pixel_tam"])

    # Calcular el GSD
    GSD = (sensor_width_mm * altitude_m) / (image_width_px * focal_distance_mm)
else:
    print("El archivo JSON está vacío o mal formado.")

# Leer la imagen
imagen = cv2.imread(imagen_path)
binary_image = cv2.imread('Imagenes/binarizada.jpg', cv2.IMREAD_GRAYSCALE)

contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Crear una imagen para dibujar el contorno
contour_image = np.zeros_like(binary_image)
cv2.drawContours(contour_image, contours, -1, (255), 1)

# Calcular el perímetro
perimeter = sum(cv2.arcLength(contour, closed=True) for contour in contours)
perimeter_m = perimeter * GSD

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
    cv2.putText(panel, f"Area: {total_area_m2:.2f} m²", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Botones para registrar y descartar
    button_height = 60  # Alto de los botones
    cv2.rectangle(panel, (10, 120), (240, 120 + button_height), (180, 180, 180), -1)  # Registrar
    cv2.putText(panel, "Registrar Resultado", (15, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    cv2.rectangle(panel, (10, 200), (240, 200 + button_height), (180, 180, 180), -1)  # Descartar
    cv2.putText(panel, "Descartar Resultado", (15, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

# Función para almacenar el resultado en la base de datos y limpiar las carpetas
def store_results():
    # Guardar los resultados en la base de datos SQLite
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()

    # Insertar los resultados
    cursor.execute(''' 
        INSERT INTO resultados (perimeter, area)
        VALUES (?, ?)
    ''', (perimeter_m, total_area_m2))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

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
            store_results()
            show_alert_message(panel, "Resultado registrado.", (0, 255, 0))  # Mostrar mensaje verde
            cv2.destroyAllWindows()  # Cerrar la ventana después del mensaje
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
