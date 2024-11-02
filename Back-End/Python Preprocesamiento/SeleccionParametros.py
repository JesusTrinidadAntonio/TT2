import subprocess
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog

# Variables globales para almacenar las respuestas
respuestas_colores = None
respuestas_tamano = None
ruta_imagen = None

# Función para manejar el clic en el botón de selección de imagen
def seleccionar_imagen():
    global ruta_imagen
    ruta_imagen = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
    )
    if ruta_imagen:
        messagebox.showinfo("Imagen seleccionada", f"Imagen: {ruta_imagen}")

# Función para manejar el clic en el botón de guardar respuestas
def guardar_respuestas():
    global respuestas_colores, respuestas_tamano
    respuestas_colores = entrada_colores.get()
    respuestas_tamano = entrada_tamano.get()

    if not ruta_imagen or not respuestas_colores or not respuestas_tamano:
        messagebox.showerror("Error", "Por favor llena todos los campos.")
        return

    ventana.destroy()

    # Ejecuta el script Python especificando el intérprete y pasando los argumentos
    subprocess.run([
        "python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Elegir_color.py",
        respuestas_colores, respuestas_tamano, ruta_imagen
    ])

# Configuración de la ventana principal
ventana = Tk()
ventana.title("Formulario de Datos")
ventana.geometry("400x300")

# Pregunta 1: Cantidad de colores en el cuerpo de agua
Label(ventana, text="¿Cuántos colores tiene el cuerpo de agua?").pack(pady=5)
entrada_colores = Entry(ventana)
entrada_colores.pack(pady=5)

# Pregunta 2: Tamaño del objeto de referencia
Label(ventana, text="¿Qué tamaño tiene el objeto de referencia en metros cuadrados?").pack(pady=5)
entrada_tamano = Entry(ventana)
entrada_tamano.pack(pady=5)

# Botón para seleccionar la imagen
boton_seleccionar_imagen = Button(ventana, text="Seleccionar imagen", command=seleccionar_imagen)
boton_seleccionar_imagen.pack(pady=10)

# Botón para guardar las respuestas
boton_guardar = Button(ventana, text="Guardar respuestas", command=guardar_respuestas)
boton_guardar.pack(pady=10)

# Ejecutar el loop principal
ventana.mainloop()