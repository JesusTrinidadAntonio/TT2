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
        imagen_G = cv2.GaussianBlur(imagen, (5, 5), 0)
        imagen_MB= cv2.medianBlur(imagen_G, 5)
        imagen_B = cv2.bilateralFilter(imagen_MB ,d=9, sigmaColor=75, sigmaSpace=75)
        

        # Crear ventanas con un tamaño personalizado
        cv2.namedWindow('Imagen original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen original', 600, 400)  # Cambia las dimensiones a tu gusto
        
        cv2.namedWindow('Filtro 1 (GaussianBlur)', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtro 1 (GaussianBlur)', 600, 400)
        
        cv2.namedWindow('Filtro 2 (MedianBlur)', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtro 2 (MedianBlur)', 600, 400)

        cv2.namedWindow('Filtro 3(Bilateral)', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Filtro 3(Bilateral)', 600, 400)

        # Mostrar las imágenes en las ventanas con el tamaño especificado
        cv2.imshow('Imagen original', imagen)
        cv2.imshow('Filtro 1 (GaussianBlur)', imagen_G)
        cv2.imshow('Filtro 2 (MedianBlur)', imagen_MB)
        cv2.imshow('Filtro 3(Bilateral)',imagen_B)

        # Esperar a que se cierre la ventana
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se pudo cargar la imagen.")
else:
    print("No se seleccionó ninguna imagen.")
