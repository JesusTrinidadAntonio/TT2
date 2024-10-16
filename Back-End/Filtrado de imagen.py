import cv2
import tkinter as tk
from tkinter import filedialog

# Crear una ventana oculta de tkinter
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

# Abrir el diálogo para seleccionar una imagen
ruta_imagen = filedialog.askopenfilename(title='Selecciona una imagen', 
                                         filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png *.bmp *.tiff')])

# Verificar si se seleccionó una imagen
if ruta_imagen:
    # Cargar la imagen seleccionada usando OpenCV
    imagen = cv2.imread(ruta_imagen)

    if imagen is not None:
        # Aplicar el filtro de desenfoque gaussiano
        imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)

        # Aplicar el filtro bilateral
        imagen_filtrada = cv2.bilateralFilter(imagen_suavizada, d=9, sigmaColor=75, sigmaSpace=75)

        # Crear ventanas con un tamaño personalizado
        cv2.namedWindow('Imagen original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen original', 600, 400)  # Cambia las dimensiones a tu gusto
        
        cv2.namedWindow('Imagen suavizada (GaussianBlur)', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen suavizada (GaussianBlur)', 600, 400)
        
        cv2.namedWindow('Imagen filtrada (Bilateral)', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen filtrada (Bilateral)', 600, 400)

        # Mostrar las imágenes en las ventanas con el tamaño especificado
        cv2.imshow('Imagen original', imagen)
        cv2.imshow('Imagen suavizada (GaussianBlur)', imagen_suavizada)
        cv2.imshow('Imagen filtrada (Bilateral)', imagen_filtrada)

        # Esperar a que se cierre la ventana
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se pudo cargar la imagen.")
else:
    print("No se seleccionó ninguna imagen.")
