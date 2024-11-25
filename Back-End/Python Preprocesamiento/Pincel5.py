import cv2
import numpy as np

# Variables globales
drawing = False  # Verdadero si el mouse está presionado
erasing = False
brush_size = 5  # Tamaño del pincel
color_solid = (0, 0, 255)  # Rojo sólido
mostrar = True
flood_fill_mode = False
ultimo_punto = None  # Guardar la última posición del mouse

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

    if event == cv2.EVENT_LBUTTONDOWN:
        if flood_fill_mode:

            flood_fill_copy = segmented_image.copy()
            flood_fill_mask = np.zeros((segmented_image.shape[0] + 2, segmented_image.shape[1] + 2), np.uint8)
            cv2.floodFill(flood_fill_copy, flood_fill_mask, (x, y), color_solid, loDiff=(20, 20, 20), upDiff=(20, 20, 20))

            # Transferir los píxeles seleccionados a la máscara
            filled_area = (flood_fill_copy == color_solid).all(axis=2)

            if np.all(mask[y, x] == color_solid): # Si ya se ha pintado esa zona, se borra
                mask[filled_area] = 0
            else:
                mask[filled_area] = color_solid
        else:
            # Activar modo de dibujo normal
            drawing = True
            ultimo_punto = (x, y)  # Guardamos la primera posición


    elif event == cv2.EVENT_MOUSEWHEEL:
            # Si el desplazamiento es positivo, la rueda sube; si es negativo, la rueda baja
            if flags > 0:
                brush_size = min(brush_size + 5, 100)
            else:
                brush_size = max(brush_size - 5, 1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and not flood_fill_mode:
            # Dibuja una línea desde el último punto hasta el actual
            if ultimo_punto:
                if not erasing:
                    cv2.line(mask, ultimo_punto, (x, y), color_solid, brush_size)
                else:
                    cv2.line(mask, ultimo_punto, (x, y), (0, 0, 0), brush_size)
            ultimo_punto = (x, y)  # Actualizamos la última posición del mouse

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ultimo_punto = None  # Reiniciar al soltar el botón del mouse

# Cargar la imagen
image = cv2.imread('Imagenes/ImagenAplanada.jpg')
if image is None:
    raise ValueError("No se pudo cargar la imagen.")

segmented_image = preprocess_image(image, k=4)
# Crear la máscara (con un canal alfa para la transparencia)
mask = np.zeros_like(image, dtype=np.uint8)

# Crear una ventana y asignar la función de callback
cv2.namedWindow('Paint')
cv2.setMouseCallback('Paint', paint)

while True:
    
    # Mostrar la máscara en la imagen original con transparencia
    combined_original = cv2.addWeighted(image, 1, mask, 0.4, 0)
    # Mostrar la máscara en la imagen segmentada sin transparencia (rojo sólido)
    combined_segmented = cv2.addWeighted(segmented_image, 1, mask, 1.0, 0)

    # Alternar entre la imagen original y la segmentada
    imagen = combined_original if mostrar else combined_segmented

    # Mostrar la imagen combinada
    cv2.imshow('Paint', imagen)

    # Salir con la tecla ESC
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Tecla ESC para salir
        break
    elif key == ord('z'):  # Alternar entre imagen segmentada y original
        mostrar = not mostrar
    elif key == ord('e'):  # Alternar entre imagen segmentada y original
        if flood_fill_mode:
            flood_fill_mode = False
        erasing = not erasing
    elif key == ord('f'):  # Alternar entre modo floodFill y pintura normal
        flood_fill_mode = not flood_fill_mode
        print("Modo Flood Fill" if flood_fill_mode else "Modo Pintura Normal")
    elif key == ord('s'):  # Guardar la máscara en binario
        # Convertir la máscara en binario: píxeles rojos a 1, resto a 0
        mask_binary = np.where((mask[:, :, 2] == 255), 1, 0).astype(np.uint8) * 255
        cv2.imwrite('Imagenes/pincel_masked.png', mask_binary)
        print("Máscara guardada en formato binario como pincel_masked.png")

# Limpiar y cerrar ventanas
cv2.destroyAllWindows()
