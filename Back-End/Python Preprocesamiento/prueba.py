import sys

# Captura los argumentos de línea de comandos
if len(sys.argv) > 2:
    respuestas_colores = sys.argv[1]
    respuestas_tamano = sys.argv[2]
    print("Colores:", respuestas_colores)
    print("Tamaño:", respuestas_tamano)
else:
    print("No se proporcionaron argumentos suficientes.")
