import cv2
import numpy as np
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
        for i in range(10):
            imagen_G = cv2.GaussianBlur(imagen, (5, 5), 0)
            imagen_MB = cv2.medianBlur(imagen_G, 5)
            imagen_B = cv2.bilateralFilter(imagen_MB, d=9, sigmaColor=75, sigmaSpace=75)
    
        # Convertir la imagen de BGR a HSV
        imagen_hsv = cv2.cvtColor(imagen_B, cv2.COLOR_BGR2HSV)

        # Multiplicar el canal de saturación por un factor para aumentarlo
        factor_saturacion = 1.5  # Puedes ajustar este valor
        imagen_hsv[:, :, 1] = np.clip(imagen_hsv[:, :, 1] * factor_saturacion, 0, 255)
        
        # Convertir la imagen de vuelta a BGR
        imagen_saturada = cv2.cvtColor(imagen_hsv, cv2.COLOR_HSV2BGR)

        # Crear ventanas con un tamaño personalizado
        cv2.namedWindow('Imagen original', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen original', 600, 400)  # Cambia las dimensiones a tu gusto

        cv2.namedWindow('Imagen Filtrada', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen Filtrada', 600, 400)  # Cambia las dimensiones a tu gusto

        cv2.namedWindow('Imagen Saturada', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen Saturada', 600, 400)  # Cambia las dimensiones a tu gusto

        # Mostrar las imágenes en las ventanas con el tamaño especificado
        cv2.imshow('Imagen original', imagen)
        cv2.imshow('Imagen Filtrada', imagen_B)
        cv2.imshow('Imagen Saturada', imagen_saturada)
        cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/ImagenFiltrada.jpg', imagen_B)
        cv2.imwrite('C:/Users/jesus/Documents/TT2/Imagenes/ImagenSaturada.jpg', imagen_saturada)



        # Esperar a que se cierre la ventana
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se pudo cargar la imagen.")
else:
    print("No se seleccionó ninguna imagen.")
