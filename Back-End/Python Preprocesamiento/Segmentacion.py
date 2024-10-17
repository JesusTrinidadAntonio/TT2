import cv2
import numpy as np
from sklearn.cluster import KMeans
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
    # Cargar la imagen seleccionada
    imagen = cv2.imread(ruta_imagen)

    if imagen is not None:
        # Cambiar la forma de la imagen para KMeans
        pixels = imagen.reshape(-1, 3)

        # Aplicar KMeans
        kmeans = KMeans(n_clusters=2, random_state=0)
        kmeans.fit(pixels)

        # Obtener los labels
        labels = kmeans.labels_
        segmented_image = labels.reshape(imagen.shape[:2])  # Volver a dar forma a la imagen segmentada

        # Mostrar la imagen original y la segmentada
        cv2.imshow('Imagen original', imagen)
        cv2.imshow('Imagen segmentada', segmented_image.astype(np.uint8) * 255)  # Convertir a 0-255 para mostrar
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se pudo cargar la imagen.")
else:
    print("No se seleccionó ninguna imagen.")

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
        # Remodelar la imagen para ser una lista de píxeles RGB
        pixeles = imagen.reshape(-1, 3)

        # Aplicar K-means para segmentar la imagen
        kmeans = KMeans(n_clusters=2, random_state=0)
        kmeans.fit(pixeles)

        # Reemplazar cada píxel con el color promedio de su grupo
        pixeles_segmentados = kmeans.cluster_centers_[kmeans.labels_]

        # Convertir los píxeles segmentados a valores enteros en el rango 0-255
        pixeles_segmentados = np.uint8(pixeles_segmentados)

        # Reshape de vuelta a la forma original de la imagen
        imagen_segmentada = pixeles_segmentados.reshape(imagen.shape)

        # Mostrar la imagen segmentada
        cv2.imshow('Imagen segmentada', imagen_segmentada)


        # Esperar a que se cierre la ventana
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No se pudo cargar la imagen.")
else:
    print("No se seleccionó ninguna imagen.")
