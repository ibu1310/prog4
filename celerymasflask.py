from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from celery import Celery
import redis
import json

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_password'

mail = Mail(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['REDIS_URL'],
        broker=app.config['REDIS_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

@celery.task
def send_email_async(subject, body, to):
    msg = Message(subject, recipients=[to])
    msg.body = body
    with app.app_context():
        mail.send(msg)

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    data = request.json
    subject = data['subject']
    body = data['body']
    to = data['to']
    send_email_async.apply_async(args=[subject, body, to])
    return jsonify({"message": "Correo en proceso de envío"}), 200

@app.route('/articulos', methods=['POST'])
def agregar_articulo():
    data = request.json
    articulo_id = client.incr('articulo_id')
    articulo = {'id': articulo_id, 'nombre': data['nombre'], 'categoria': data['categoria'], 'precio': data['precio']}
    client.set(f'articulo:{articulo_id}', json.dumps(articulo))
    return jsonify(articulo), 201

@app.route('/articulos/<int:id>', methods=['PUT'])
def actualizar_articulo(id):
    data = request.json
    articulo = client.get(f'articulo:{id}')
    if articulo:
        articulo = json.loads(articulo)
        articulo['nombre'] = data['nombre']
        articulo['categoria'] = data['categoria']
        articulo['precio'] = data['precio']
        client.set(f'articulo:{id}', json.dumps(articulo))
        return jsonify(articulo)
    return jsonify({'error': 'Artículo no encontrado'}), 404

@app.route('/articulos/<int:id>', methods=['DELETE'])
def eliminar_articulo(id):
    if client.delete(f'articulo:{id}'):
        return jsonify({'message': 'Artículo eliminado con éxito'}), 200
    return jsonify({'error': 'Artículo no encontrado'}), 404

@app.route('/articulos', methods=['GET'])
def ver_articulos():
    articulos_keys = client.keys('articulo:*')
    articulos = [json.loads(client.get(key)) for key in articulos_keys]
    return render_template('articulos.html', articulos=articulos)

@app.route('/articulos/<int:id>', methods=['GET'])
def buscar_articulo(id):
    articulo = client.get(f'articulo:{id}')
    if articulo:
        articulo = json.loads(articulo)
        return render_template('articulo.html', articulo=articulo)
    return render_template('error.html', mensaje='Artículo no encontrado'), 404

if __name__ == '__main__':
    app.run()