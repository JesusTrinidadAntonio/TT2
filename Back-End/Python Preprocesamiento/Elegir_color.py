import cv2
import numpy as np

# Lista para almacenar los rangos mínimos y máximos de colores HSV
rango_colores_hsv = []

# Variables para almacenar el mínimo y máximo
hsv_min = None
hsv_max = None

# Número máximo de rangos de colores a seleccionar
num_rangos_a_seleccionar = 3  # Puedes ajustar este número según tus necesidades

# Función que se llama cada vez que se hace clic en la imagen
def seleccion_color(event, x, y, flags, param):
    global hsv_min, hsv_max, rango_colores_hsv
    
    if event == cv2.EVENT_LBUTTONDOWN:  # Evento de clic izquierdo
        # Obtener el color en el punto (x, y) de la imagen
        color_bgr = img[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"Color seleccionado (BGR): {color_bgr} | (HSV): {color_hsv}")
        
        # Si no se ha seleccionado aún el mínimo, lo asignamos
        if hsv_min is None:
            hsv_min = color_hsv
            print(f"HSV mínimo seleccionado: {hsv_min}")
        # Si el mínimo ya está seleccionado, asignamos el máximo
        elif hsv_max is None:
            hsv_max = color_hsv
            print(f"HSV máximo seleccionado: {hsv_max}")
            # Guardamos el rango de colores
            rango_colores_hsv.append({
                "hsv_min": hsv_min.tolist(),
                "hsv_max": hsv_max.tolist()
            })
            # Reiniciar los valores de mínimo y máximo para seleccionar más rangos
            hsv_min = None
            hsv_max = None

            # Si ya hemos seleccionado el número máximo de rangos, cerramos la ventana
            if len(rango_colores_hsv) >= num_rangos_a_seleccionar:
                print("Se ha alcanzado el número máximo de rangos seleccionados.")
                cv2.destroyAllWindows()

# Cargar la imagen
img = cv2.imread("C:/Users/jesus/Documents/TT2/Imagenes/imagen_saturada.jpg")

# Crear una ventana para mostrar la imagen
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', seleccion_color)

# Mostrar la imagen y permitir la selección de colores
while True:
    cv2.imshow('Imagen', img)
    
    # Salir del bucle cuando se cierran todas las ventanas
    if cv2.getWindowProperty('Imagen', cv2.WND_PROP_VISIBLE) < 1:
        break

# Mostrar los rangos de colores HSV seleccionados
print("Rangos de colores HSV seleccionados:")
for rango in rango_colores_hsv:
    print(f"HSV Mínimo: {rango['hsv_min']} | HSV Máximo: {rango['hsv_max']}")