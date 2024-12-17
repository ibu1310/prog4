from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

API_URL = "http://localhost:5000/api/articulos"

def obtener_articulos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []


def agregar_articulo_api(data):
    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        return response.json()
    return None


def actualizar_articulo_api(id, data):
    response = requests.put(f"{API_URL}/{id}", json=data)
    if response.status_code == 200:
        return response.json()
    return None


def eliminar_articulo_api(id):
    response = requests.delete(f"{API_URL}/{id}")
    return response.status_code == 200

def obtener_articulo_por_id(id):
    response = requests.get(f"{API_URL}/{id}")
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/articulos', methods=['POST'])
def agregar_articulo():
    data = request.json
    articulo = agregar_articulo_api(data)
    if articulo:
        return jsonify(articulo), 201
    return jsonify({'error': 'No se pudo agregar el artículo'}), 400

@app.route('/articulos/<int:id>', methods=['PUT'])
def actualizar_articulo(id):
    data = request.json
    articulo = actualizar_articulo_api(id, data)
    if articulo:
        return jsonify(articulo)
    return jsonify({'error': 'Artículo no encontrado'}), 404

@app.route('/articulos/<int:id>', methods=['DELETE'])
def eliminar_articulo(id):
    if eliminar_articulo_api(id):
        return jsonify({'message': 'Artículo eliminado con éxito'}), 200
    return jsonify({'error': 'Artículo no encontrado'}), 404

@app.route('/articulos', methods=['GET'])
def ver_articulos():
    articulos = obtener_articulos()
    return render_template('articulos.html', articulos=articulos)

@app.route('/articulos/<int:id>', methods=['GET'])
def buscar_articulo(id):
    articulo = obtener_articulo_por_id(id)
    if articulo:
        return render_template('articulo.html', articulo=articulo)
    return render_template('error.html', mensaje='Artículo no encontrado'), 404

if __name__ == '__main__':
    app.run(debug=True)