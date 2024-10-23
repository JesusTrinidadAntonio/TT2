import cv2
import numpy as np

# Lista para almacenar los colores seleccionados
colores_seleccionados = []

# Función que se llama cada vez que se hace clic en la imagen
def seleccion_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Evento de clic izquierdo
        # Obtener el color en el punto (x, y) de la imagen
        color_bgr = img[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"Color seleccionado (BGR): {color_bgr} | (HSV): {color_hsv}")
        
        # Agregar el color a la lista de colores seleccionados
        colores_seleccionados.append({
            "posicion": (x, y),
            "color_bgr": color_bgr.tolist(),
            "color_hsv": color_hsv.tolist()
        })

# Cargar la imagen
img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/imagen_saturada.jpg")

# Crear una ventana para mostrar la imagen
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', seleccion_color)

# Mostrar la imagen y permitir la selección de colores
while True:
    cv2.imshow('Imagen', img)
    
    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar todas las ventanas
cv2.destroyAllWindows()

# Mostrar los colores seleccionados
print("Colores seleccionados:")
for color in colores_seleccionados:
    print(f"Posición: {color['posicion']} | Color BGR: {color['color_bgr']} | Color HSV: {color['color_hsv']}")
