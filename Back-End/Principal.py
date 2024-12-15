from flask import Flask, request, jsonify, render_template,send_from_directory
from PIL import Image
import cv2
import os
import uuid
import json
import subprocess
from flask_cors import CORS

app = Flask(__name__,static_url_path='/static', static_folder='Imagenes')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Permitir solicitudes desde localhost:3000

# Carpeta donde se guardan las imágenes
app.config['IMAGENES_FOLDER'] = 'Imagenes'
os.makedirs(app.config['IMAGENES_FOLDER'], exist_ok=True)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Obtener los datos del formulario
    try:
        respuestas_colores = int(request.form['colores'])  # Cantidad de rangos de colores
        respuestas_tamano = request.form['tamano']         # Tamaño del objeto
        imagen = request.files['imagen']                    # La imagen recibida como archivo
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error al procesar los datos del formulario: {e}'}), 400

    # Guardar la imagen en un directorio específico
    if imagen:
        ruta_imagen = os.path.join('imagenes', "Cuerpo_Agua.jpg")
        imagen.save(ruta_imagen)
    else:
        return jsonify({'error': 'No se proporcionó una imagen.'}), 400

    # Verificar si la imagen se ha cargado correctamente
    imagen_cargada = cv2.imread(ruta_imagen)
    if imagen_cargada is None:
        return jsonify({'error': 'No se pudo cargar la imagen.'}), 400
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        nombre_unico = str(uuid.uuid4())
        ruta_guardado = os.path.join(ruta_base, '../pagina-web/src/public/img', f'{nombre_unico}Cuerpo_Agua.jpg')
        nombre_imagen = 'img/'f'{nombre_unico}Cuerpo_Agua.jpg'
        cv2.imwrite(ruta_guardado, imagen_cargada)

        imagen1 = {
                            'nombre_cuerpo_a' : nombre_imagen,
                   }
       
       
        try:
            with open('resultados.json', 'r') as file:
                data = []
        except (FileNotFoundError, json.JSONDecodeError):
            data = []  # Si el archivo no existe o está mal formado, inicializamos con lista vacía
       
        # Agregar los nuevos resultados
        data.append(imagen1)
       
        # Guardar los datos actualizados en el archivo resultados.json
        try:
            with open('resultados.json', 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error al guardar los resultados en 'resultados.json': {e}")
            return

    # Obtener el tamaño de la imagen con OpenCV (usamos ancho y alto directamente)
    ancho = imagen_cargada.shape[1]

    # Datos a guardar (puedes incluir el tamaño de la imagen si lo deseas)
    new_data = {
        'color': respuestas_colores,
        'tamano': respuestas_tamano,
        'imagen_tamano': ancho,  
        'ruta': ruta_imagen
    }

    # Intentar leer el archivo JSON y cargar los datos existentes
    try:
        with open('datos.json', 'r') as file:
            data = [] 
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  

    # Agregar los nuevos datos
    data.append(new_data)

    # Guardar los datos actualizados en el archivo JSON
    with open('datos.json', 'w') as file:
        json.dump(data, file, indent=4)

# Ejecución del flujo de trabajo
    try:
        # Ejecutar los scripts en orden secuencial
        subprocess.run(["python", "Filtrado y Saturacion.py"], check=True)
        subprocess.run(["python", "Color.py"], check=True)
        subprocess.run(["python", "Referencia.py"], check=True)
        subprocess.run(["python", "Deteccion.py"], check=True)
        subprocess.run(["python", "Pincel.py"], check=True)
        subprocess.run(["python", "Pixel.py"], check=True)
        subprocess.run(["python", "Area y GSD.py"], check=True)

    except subprocess.CalledProcessError as e:
        # Si algún script falla, devolvemos un error
        return jsonify({'error': f'No se completo el flujo: {str(e)}'}), 500


    # Devolver una respuesta exitosa al cliente
    return jsonify({
        'success': True,
        'message': 'Formulario procesado correctamente',
        'image_path': ruta_imagen  # Ruta donde se guardó la imagen
    })


# Ruta para devolver el JSON de resultados junto con las rutas de las imágenes
@app.route('/resultados', methods=['GET'])
def get_resultados():
    try:
        # Intentar leer el archivo 'resultados.json'
        with open('resultados.json', 'r') as file:
            resultados_data = json.load(file)
        
        return jsonify(resultados_data)

    except (FileNotFoundError, json.JSONDecodeError):
        # Si no se encuentra el archivo o hay un error con el JSON, devolver un mensaje de error
        return jsonify({'error': 'No se encontraron resultados.'}), 404

if __name__ == '__main__':
    os.makedirs('Imagenes', exist_ok=True)  # Crear el directorio si no existe
    os.makedirs('colores', exist_ok=True)  # Crear el directorio si no existe
    app.run(debug=True)