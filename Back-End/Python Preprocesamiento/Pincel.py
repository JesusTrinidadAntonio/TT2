import cv2
import numpy as np
import sys
import os
import subprocess

# Verificar y capturar argumentos
if len(sys.argv) > 3:
    ruta_mask_varios = sys.argv[1]
    respuesta_tamano = sys.argv[2]
    ruta_combinada = sys.argv[3]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar las máscaras
mask_varios = np.load(ruta_mask_varios)

# Cargar la imagen desde la ubicación especificada
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(ruta_base, 'Imagenes', 'resultado_varios_rangos.jpg')

img = cv2.imread(ruta_imagen)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Configurar dimensiones de la ventana y el área de botones
button_panel_width = 150  # Ancho del área de botones
button_panel = np.ones((img.shape[0], button_panel_width, 3), dtype=np.uint8) * 200  # Fondo gris claro

# Variables iniciales
overlay = img.copy()
output = img.copy()
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Máscara para binarización
brush_size = 10  # Tamaño de la brocha
painting = False
erasing = False
current_color = (0, 0, 255, 127)  # Color rojo transparente

# Coordenadas de los botones
button_reset = (10, 20, 140, 60)  # Coordenadas del botón de reinicio
button_save = (10, 80, 140, 120)  # Coordenadas del botón de guardar
button_close = (10, 140, 140, 180)  # Coordenadas del botón de cerrar
button_erase = (10, 200, 140, 240)  # Botón de borrado
button_manual = (10, 260, 140, 300)  # Botón de detección manual

# Variable global para almacenar la última posición del mouse
last_point = None

# Actualización de la función 'paint' con interpolación de líneas
def paint(event, x, y, flags, param):
    global painting, erasing, overlay, output, mask, last_point

    if x < img.shape[1]:  # Solo activar si se hace clic en la imagen
        if event == cv2.EVENT_LBUTTONDOWN:
            painting = True
            last_point = (x, y)  # Almacenar la posición inicial del trazo

        elif event == cv2.EVENT_LBUTTONUP:
            painting = False
            last_point = None  # Restablecer la posición al soltar el botón

        elif event == cv2.EVENT_MOUSEMOVE and painting:
            # Dibuja una línea entre el último punto y el actual
            if erasing:
                # Borrar la pintura y actualizar la máscara
                cv2.line(overlay, last_point, (x, y), img[y, x].tolist(), brush_size * 2)
                cv2.line(mask, last_point, (x, y), 0, brush_size * 2)
            else:
                # Pintar en la capa overlay con transparencia y actualizar la máscara
                cv2.line(overlay, last_point, (x, y), current_color[:3], brush_size * 2)
                cv2.line(mask, last_point, (x, y), 255, brush_size * 2)

            last_point = (x, y)  # Actualizar la última posición del mouse
            output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

    elif event == cv2.EVENT_LBUTTONDOWN:
        # Comprobar si se ha hecho clic en algún botón
        if button_reset[0] <= x - img.shape[1] <= button_reset[2] and button_reset[1] <= y <= button_reset[3]:
            # Reiniciar la máscara y la capa de pintura
            overlay = img.copy()
            output = img.copy()
            mask.fill(0)
            print("Malla roja reiniciada.")

        elif button_save[0] <= x - img.shape[1] <= button_save[2] and button_save[1] <= y <= button_save[3]:
            # Combinar la máscara actual con la máscara cargada
            combined_mask = cv2.bitwise_or(mask, mask_varios)

            # Guardar la máscara combinada como una imagen binarizada
            binary_img = np.zeros_like(img)
            binary_img[combined_mask != 0] = (255, 255, 255)
            ruta = os.path.join(ruta_base, 'Imagenes', 'binarizada.jpg')
            cv2.imwrite(ruta, binary_img)

            os.chdir(os.path.dirname(__file__))
            subprocess.run(["python", "pixel.py", str(respuesta_tamano), str(ruta_combinada)])

            cv2.destroyAllWindows()
            exit()

        elif button_close[0] <= x - img.shape[1] <= button_close[2] and button_close[1] <= y <= button_close[3]:
            # Cerrar la aplicación
            print("Cerrando aplicación.")
            cv2.destroyAllWindows()
            exit()

        elif button_erase[0] <= x - img.shape[1] <= button_erase[2] and button_erase[1] <= y <= button_erase[3]:
            # Cambiar estado de borrado
            erasing = not erasing
            print("Modo borrar activado." if erasing else "Modo borrar desactivado.")

        elif button_manual[0] <= x - img.shape[1] <= button_manual[2] and button_manual[1] <= y <= button_manual[3]:
            # Llamar al programa pincel5.py
            print("Ejecutando detección manual (pincel5.py)...")
            subprocess.run(["python", "pincel5.py", ruta_mask_varios, respuesta_tamano, ruta_combinada])

# Dibujar los botones
def draw_buttons(panel):
    # Botón de reinicio
    cv2.rectangle(panel, (button_reset[0], button_reset[1]), (button_reset[2], button_reset[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Reiniciar", (button_reset[0] + 10, button_reset[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de guardar
    cv2.rectangle(panel, (button_save[0], button_save[1]), (button_save[2], button_save[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Guardar", (button_save[0] + 20, button_save[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de cerrar
    cv2.rectangle(panel, (button_close[0], button_close[1]), (button_close[2], button_close[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Cerrar", (button_close[0] + 20, button_close[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de borrar
    erase_button_color = (255, 255, 255) if erasing else (180, 180, 180)
    cv2.rectangle(panel, (button_erase[0], button_erase[1]), (button_erase[2], button_erase[3]), erase_button_color, -1)
    cv2.putText(panel, "Borrar", (button_erase[0] + 30, button_erase[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de detección manual
    cv2.rectangle(panel, (button_manual[0], button_manual[1]), (button_manual[2], button_manual[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Manual", (button_manual[0] + 30, button_manual[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Configurar el callback del mouse en la imagen
cv2.namedWindow("Paint Tool")
cv2.setMouseCallback("Paint Tool", paint)

while True:
    # Crear una imagen combinada de la imagen y el panel de botones
    combined_output = np.hstack((output, button_panel))
    draw_buttons(button_panel)

    # Mostrar la imagen combinada
    cv2.imshow("Paint Tool", combined_output)
    
    # Esc para salir
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()