import cv2
import numpy as np
import sys
import os
import subprocess

# Verificar y capturar argumentos
if len(sys.argv) > 2:
    ruta_imagen_saturada = sys.argv[1]
    respuesta_tamano = sys.argv[2]  # No utilizado directamente, pero se mantiene para consistencia
else:
    print("No se proporcionaron argumentos suficientes.")
    sys.exit(1)

# Cargar la imagen saturada
img = cv2.imread(ruta_imagen_saturada)
if img is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen_saturada}")
    sys.exit(1)

# Convertir la imagen a HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def procesar_varios_rangos():
    colores_hsv = []
    try:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_base, "colores", "colores_seleccionados.txt")
        with open(ruta_archivo, "r") as f:
            hsv_values = []
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Saltar líneas vacías
                
                # Validar que la línea contiene "HSV: "
                if "HSV: " not in line:
                    print(f"Línea con formato inesperado: {line}")
                    continue
                
                # Extraer el array HSV
                try:
                    hsv_value = np.array([int(x) for x in line.split("HSV: ")[1].strip()[1:-1].split(", ")])
                    hsv_values.append(hsv_value)
                except Exception as e:
                    print(f"Error al procesar la línea: {line}")
                    print(f"Detalle del error: {e}")
                    continue
                
            # Generar rangos mínimos y máximos
            if hsv_values:
                hsv_values = np.array(hsv_values)
                hsv_min = np.min(hsv_values, axis=0)
                hsv_max = np.max(hsv_values, axis=0)
                
                # Aplicar tolerancia
                tolerancia = np.array([10, 40, 50])  # Ajustar tolerancia para cada componente
                hsv_min = np.clip(hsv_min - tolerancia, 0, 255)
                hsv_max = np.clip(hsv_max + tolerancia, 0, 255)
                
                # Guardar los rangos calculados
                colores_hsv.append((hsv_min, hsv_max))
            else:
                print("No se encontraron valores HSV válidos en el archivo.")
    except FileNotFoundError:
        print("El archivo colores_seleccionados.txt no se encontró.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al procesar el archivo de colores: {e}")
        sys.exit(1)

    # Crear la máscara total combinando todos los rangos con tolerancia
    mask_total = None
    for hsv_min, hsv_max in colores_hsv:
        mask = cv2.inRange(img_hsv, hsv_min, hsv_max)
        mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar el contorno más grande
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        mask_largest = np.zeros_like(mask_total)
        cv2.drawContours(mask_largest, [largest_contour], -1, 255, thickness=cv2.FILLED)
        mask_total = mask_largest
    else:
        print("No se encontraron regiones en la máscara.")

    # Guardar la máscara como archivo .npy para que Pincel.py la pueda leer
    ruta_mask_varios = os.path.join(ruta_base, 'colores', 'mascara_varios_rangos.npy')
    np.save(ruta_mask_varios, mask_total)

    # Aplicar la máscara a la imagen original y guardar el resultado
    resultado = cv2.bitwise_and(img, img, mask=mask_total)
    ruta_imagen_lago = os.path.join(ruta_base, 'Imagenes', 'resultado_varios_rangos.jpg')
    cv2.imwrite(ruta_imagen_lago, resultado)
    print("Imagen procesada con varios rangos guardada como resultado_varios_rangos.jpg")

    return ruta_mask_varios  # Retornar la ruta de la máscara guardada



def procesar_un_rango():
    try:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_base, "colores", "rango.txt")
        with open(ruta_archivo, "r") as f:
            line = f.readline().strip()
            if line:
                # Extraer los valores mínimos y máximos del archivo
                min_part = line.split("], Max: ")[0]
                max_part = line.split("], Max: ")[1]

                # Convertir el texto a arrays de NumPy y aplicar una tolerancia
                hsv_min = np.array([int(x) for x in min_part.split(": ")[1].strip()[1:-1].split(", ")])
                hsv_max = np.array([int(x) for x in max_part.strip()[1:-1].split(", ")])

                # Aplicar tolerancia
                tolerancia = np.array([10, 40, 50])  # Ajustar tolerancia para cada componente
                hsv_min = np.clip(hsv_min - tolerancia, 0, 255)
                hsv_max = np.clip(hsv_max + tolerancia, 0, 255)

    except FileNotFoundError:
        print("El archivo rango.txt no se encontró.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al procesar el archivo de colores: {e}")
        sys.exit(1)

    # Crear la máscara para el único rango de color
    mask = cv2.inRange(img_hsv, hsv_min, hsv_max)

    # Guardar la máscara como archivo .npy para que Pincel.py la pueda leer
    ruta_mask_uno = os.path.join(ruta_base, 'colores', 'mascara_un_rango.npy')
    np.save(ruta_mask_uno, mask)

    # Aplicar la máscara a la imagen original y guardar el resultado
    ruta_imagen_objeto = os.path.join(ruta_base, 'Imagenes', 'resultado_un_rango.jpg')
    resultado = cv2.bitwise_and(img, img, mask=mask)
    cv2.imwrite(ruta_imagen_objeto, resultado)
    print("Imagen procesada con un rango guardada como resultado_un_rango.png")

    return ruta_mask_uno  # Retornar la ruta de la máscara guardada


# Ejecutar ambas funciones y obtener las rutas de las máscaras guardadas
ruta_mask_varios = procesar_varios_rangos()
ruta_mask_uno = procesar_un_rango()

# Ejecutar Pincel.py pasando las rutas de las máscaras como argumentos
os.chdir(os.path.dirname(__file__))
subprocess.run([
    "python", "Pincel.py",
    str(ruta_mask_varios), str(ruta_mask_uno), str(respuesta_tamano)
])