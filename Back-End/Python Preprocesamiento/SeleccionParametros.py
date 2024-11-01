import subprocess  # Importamos subprocess para ejecutar el programa externo
from tkinter import Tk, Label, Entry, Button, messagebox


respuestas_colores = None
respuestas_tamano = None


def guardar_respuestas():
    global respuestas_colores, respuestas_tamano
    respuestas_colores = entrada_colores.get()
    respuestas_tamano = entrada_tamano.get()

    ventana.destroy()
    
    subprocess.run(["python", "C:/Users/jesus/Documents/TT2/Back-End/Python Preprocesamiento/Elegir_color.py",respuestas_colores,respuestas_tamano])
 

ventana = Tk()
ventana.title("Formulario de Datos")
ventana.geometry("400x200")


Label(ventana, text="¿Cuántos colores tiene el cuerpo de agua?").pack(pady=5)
entrada_colores = Entry(ventana)
entrada_colores.pack(pady=5)

Label(ventana, text="¿Qué tamaño tiene el objeto de referencia en metros cuadrados?").pack(pady=5)
entrada_tamano = Entry(ventana)
entrada_tamano.pack(pady=5)

boton_guardar = Button(ventana, text="Guardar respuestas", command=guardar_respuestas)
boton_guardar.pack(pady=10)


ventana.mainloop()


