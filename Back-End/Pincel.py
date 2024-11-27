import cv2
import numpy as np
import sys
import os
import subprocess

# Verificar y capturar argumentos
if len(sys.argv) > 4:
    ruta_mask_varios = sys.argv[1]
    respuesta_tamano = sys.argv[2]
    ruta_combinada = sys.argv[3]
    ruta_imagen_aplanada = sys.argv[4]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar las máscaras
mask_varios = np.load(ruta_mask_varios)

# Cargar la imagen de resultados y la imagen aplanada
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(ruta_base, 'Imagenes', 'resultado_varios_rangos.jpg')
img = cv2.imread(ruta_imagen)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Cargar la imagen aplanada
imagen_aplanada = cv2.imread(ruta_imagen_aplanada)
if imagen_aplanada is None:
    print("Error: No se pudo cargar la imagen aplanada.")
    exit()

# Redimensionar la imagen aplanada a las mismas dimensiones de la imagen de resultado
imagen_aplanada = cv2.resize(imagen_aplanada, (img.shape[1], img.shape[0]))

# Configurar dimensiones de la ventana y el área de botones
button_panel_width = 150  # Ancho del área de botones
panel_height, panel_width = img.shape[:2]
button_panel = np.ones((panel_height, button_panel_width, 3), dtype=np.uint8) * 200  # Fondo gris claro

# Variables iniciales
overlay = np.zeros_like(img)  # Capa para pintar trazos del pincel
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Máscara para binarización
brush_size = 10  # Tamaño de la brocha
painting = False
erasing = False
current_color = (0, 0, 255)  # Color rojo

# Coordenadas de los botones
button_reset = (10, 20, 140, 60)
button_save = (10, 80, 140, 120)
button_close = (10, 140, 140, 180)
button_erase = (10, 200, 140, 240)
button_manual = (10, 260, 140, 300)

# Variable global para almacenar la última posición del mouse
last_point = None

# Función para manejar los eventos del pincel
def paint(event, x, y, flags, param):
    global painting, erasing, overlay, mask, last_point, brush_size

    # Solo permitir pintar en el área de la imagen (excluir el panel de botones)
    if x < img.shape[1]:
        if event == cv2.EVENT_LBUTTONDOWN:
            painting = True
            last_point = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            painting = False
            last_point = None

        elif event == cv2.EVENT_MOUSEMOVE and painting:
            if erasing:
                # Borrar en el overlay y la máscara
                cv2.line(overlay, last_point, (x, y), (0, 0, 0), brush_size * 2)
                cv2.line(mask, last_point, (x, y), 0, brush_size * 2)
            else:
                # Pintar en el overlay y actualizar la máscara
                cv2.line(overlay, last_point, (x, y), current_color, brush_size * 2)
                cv2.line(mask, last_point, (x, y), 255, brush_size * 2)
            last_point = (x, y)

    # Detectar clics en los botones
    elif event == cv2.EVENT_LBUTTONDOWN:
        x_button = x - img.shape[1]  # Ajustar coordenada x para el panel
        if button_reset[0] <= x_button <= button_reset[2] and button_reset[1] <= y <= button_reset[3]:
            overlay.fill(0)
            mask.fill(0)
            print("Reiniciado.")
        elif button_save[0] <= x_button <= button_save[2] and button_save[1] <= y <= button_save[3]:
            print("Guardando...")
            # Combinar la máscara del pincel con la máscara de varios rangos
            combined_mask = cv2.bitwise_or(mask, mask_varios)
            # Guardar la máscara combinada como una imagen binarizada
            binary_img = np.zeros_like(img)
            binary_img[combined_mask > 0] = (255, 255, 255)
            ruta_guardado = os.path.join(ruta_base, 'Imagenes', 'binarizada.jpg')
            cv2.imwrite(ruta_guardado, binary_img)
            print("Guardado completado.")
            subprocess.run(["python", "pixel.py", str(respuesta_tamano), str(ruta_combinada)])
            cv2.destroyAllWindows()
            exit()
        elif button_close[0] <= x_button <= button_close[2] and button_close[1] <= y <= button_close[3]:
            print("Cerrando.")
            cv2.destroyAllWindows()
            exit()
        elif button_erase[0] <= x_button <= button_erase[2] and button_erase[1] <= y <= button_erase[3]:
            erasing = not erasing
            print("Borrado activado." if erasing else "Borrado desactivado.")
        elif button_manual[0] <= x_button <= button_manual[2] and button_manual[1] <= y <= button_manual[3]:
            print("Ejecutando detección manual.")
            subprocess.run(["python", "pincel5.py", str(respuesta_tamano), str(ruta_combinada), str(ruta_imagen_aplanada)])
            cv2.destroyAllWindows()
            exit()

    # Detectar el desplazamiento de la rueda del ratón para cambiar el tamaño del pincel
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Rueda hacia arriba
            brush_size += 1
        elif flags < 0:  # Rueda hacia abajo
            brush_size = max(1, brush_size - 1)  # Evitar que el tamaño sea menor a 1
        print(f"Tamaño del pincel: {brush_size}")

# Dibujar los botones
def draw_buttons(panel):
    cv2.rectangle(panel, (button_reset[0], button_reset[1]), (button_reset[2], button_reset[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Reiniciar", (button_reset[0] + 10, button_reset[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.rectangle(panel, (button_save[0], button_save[1]), (button_save[2], button_save[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Guardar", (button_save[0] + 20, button_save[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.rectangle(panel, (button_close[0], button_close[1]), (button_close[2], button_close[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Cerrar", (button_close[0] + 20, button_close[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    erase_color = (255, 255, 255) if erasing else (180, 180, 180)
    cv2.rectangle(panel, (button_erase[0], button_erase[1]), (button_erase[2], button_erase[3]), erase_color, -1)
    cv2.putText(panel, "Borrar", (button_erase[0] + 20, button_erase[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.rectangle(panel, (button_manual[0], button_manual[1]), (button_manual[2], button_manual[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Manual", (button_manual[0] + 20, button_manual[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Configurar el callback del mouse
cv2.namedWindow("Paint Tool")
cv2.setMouseCallback("Paint Tool", paint)

while True:
    # Fusionar la imagen aplanada con transparencia
    imagen_fusionada = cv2.addWeighted(imagen_aplanada, 0.3, img, 0.7, 0)
    # Combinar el overlay sobre la imagen fusionada
    resultado = cv2.addWeighted(imagen_fusionada, 1, overlay, 1, 0)
    # Combinar con el panel de botones
    combinado_final = np.hstack((resultado, button_panel))
    draw_buttons(button_panel)
    # Mostrar la ventana
    cv2.imshow("Paint Tool", combinado_final)

    # Salir con la tecla 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
