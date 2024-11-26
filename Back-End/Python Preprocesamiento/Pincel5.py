import cv2
import numpy as np
import sys
import os
import subprocess

# Verificar y capturar argumentos de línea de comandos
if len(sys.argv) > 2:  
    respuesta_tamano = float(sys.argv[1])  # Tamaño del objeto de referencia
    ruta_combinada = sys.argv[2]
    ruta_imagen_aplanada = sys.argv[3]
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Variables globales
drawing = False  # Verdadero si el mouse está presionado
erasing = False
brush_size = 5  # Tamaño del pincel
color_solid = (0, 0, 255)  # Rojo sólido
mostrar = True
flood_fill_mode = False
ultimo_punto = None  # Guardar la última posición del mouse

# Dimensiones del panel lateral para el menú
menu_width = 150  # Ancho del menú

def preprocess_image(image, k=3):
    bilateral_filtered = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    pixel_values = np.float32(bilateral_filtered.reshape((-1, 3)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()].reshape(bilateral_filtered.shape)
    return segmented_image

# Función de callback del mouse
def paint(event, x, y, flags, param):
    global drawing, erasing, flood_fill_mode, mask, segmented_image, ultimo_punto, brush_size, color_solid

    if x < image.shape[1]:  # Solo dibujar en el área de la imagen, no en el menú
        if event == cv2.EVENT_LBUTTONDOWN:
            if flood_fill_mode:
                flood_fill_copy = segmented_image.copy()
                flood_fill_mask = np.zeros((segmented_image.shape[0] + 2, segmented_image.shape[1] + 2), np.uint8)
                cv2.floodFill(flood_fill_copy, flood_fill_mask, (x, y), color_solid, loDiff=(20, 20, 20), upDiff=(20, 20, 20))

                # Transferir los píxeles seleccionados a la máscara
                filled_area = (flood_fill_copy == color_solid).all(axis=2)

                if np.all(mask[y, x] == color_solid):  # Si ya se ha pintado esa zona, se borra
                    mask[filled_area] = 0
                else:
                    mask[filled_area] = color_solid
            else:
                drawing = True
                ultimo_punto = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing and not flood_fill_mode:
                if ultimo_punto:
                    if not erasing:
                        cv2.line(mask, ultimo_punto, (x, y), color_solid, brush_size)
                    else:
                        cv2.line(mask, ultimo_punto, (x, y), (0, 0, 0), brush_size)
                ultimo_punto = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            ultimo_punto = None  # Reiniciar al soltar el botón del mouse

# Función para manejar clics en el menú
def handle_menu_click(x, y):
    global mostrar, erasing, flood_fill_mode, mask
    if 20 <= y <= 60:  # Alternar entre imagen original y segmentada
        mostrar = not mostrar
    elif 70 <= y <= 110:  # Alternar entre borrado y pintado
        erasing = not erasing
    elif 120 <= y <= 160:  # Alternar entre flood fill y pintura normal
        flood_fill_mode = not flood_fill_mode
    elif 170 <= y <= 210:  # Guardar la máscara
        save_mask()

# Guardar la máscara como binario
def save_mask():
    global mask
    mask_binary = np.where((mask[:, :, 2] == 255), 1, 0).astype(np.uint8) * 255
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(ruta_base, 'Imagenes', 'binarizada.jpg')
    cv2.imwrite(ruta, mask_binary)
    print("Máscara guardada en formato binario como 'binarizada.jpg'")

# Cargar la imagen
image = cv2.imread(ruta_imagen_aplanada)
if image is None:
    raise ValueError("No se pudo cargar la imagen.")

segmented_image = preprocess_image(image, k=5)
mask = np.zeros_like(image, dtype=np.uint8)  # Crear la máscara

# Crear una ventana y asignar la función de callback
cv2.namedWindow('Paint')
cv2.setMouseCallback('Paint', paint)

while True:
    # Mostrar la máscara en la imagen original con transparencia
    combined_original = cv2.addWeighted(image, 1, mask, 0.4, 0)
    combined_segmented = cv2.addWeighted(segmented_image, 1, mask, 1.0, 0)
    imagen = combined_original if mostrar else combined_segmented

    # Crear el panel del menú
    menu = np.ones((image.shape[0], menu_width, 3), dtype=np.uint8) * 200
    cv2.putText(menu, "Alternar (Z)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(menu, "Borrar (E)", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(menu, "FloodFill (F)", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(menu, "Guardar (S)", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Combinar la imagen con el menú
    combined_display = np.hstack((imagen, menu))

    # Mostrar la imagen combinada
    cv2.imshow('Paint', combined_display)

    # Manejar eventos del teclado
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Salir con ESC
        break
    elif key == ord('z'):
        mostrar = not mostrar
    elif key == ord('e'):
        erasing = not erasing
    elif key == ord('f'):
        flood_fill_mode = not flood_fill_mode
    elif key == ord('s'):
        subprocess.run(["python", "pixel.py", str(respuesta_tamano), str(ruta_combinada)])
        save_mask()
        break

cv2.destroyAllWindows()
