import sqlite3

# Crear la base de datos (si no existe)
conn = sqlite3.connect('resultados.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perimeter REAL,
        area REAL
    )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos 'resultados.db' creada con la tabla 'resultados'.")
