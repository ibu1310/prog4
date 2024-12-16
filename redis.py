from flask import Flask, request, jsonify, render_template
import redis
import json

app = Flask(__name__)

client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipes', methods=['GET'])
def list_recipes():
    keys = client.keys()
    recipes = [{"name": key, **json.loads(client.get(key))} for key in keys]
    return jsonify(recipes)

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    name = data.get('name')
    ingredients = data.get('ingredients')
    steps = data.get('steps')

    if not all([name, ingredients, steps]):
        return jsonify({"error": "All fields (name, ingredients, steps) are required."}), 400

    recipe = {
        "ingredients": ingredients,
        "steps": steps
    }
    client.set(name, json.dumps(recipe))
    return jsonify({"message": "Recipe added successfully!"}), 201

@app.route('/recipes/<name>', methods=['GET'])
def get_recipe(name):
    recipe = client.get(name)
    if recipe:
        return jsonify({"name": name, **json.loads(recipe)})
    else:
        return jsonify({"error": "Recipe not found."}), 404

@app.route('/recipes/<name>', methods=['PUT'])
def update_recipe(name):
    recipe = client.get(name)
    if recipe:
        data = request.json
        ingredients = data.get('ingredients', json.loads(recipe).get('ingredients'))
        steps = data.get('steps', json.loads(recipe).get('steps'))

        updated_recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        client.set(name, json.dumps(updated_recipe))
        return jsonify({"message": "Recipe updated successfully!"})
    else:
        return jsonify({"error": "Recipe not found."}), 404

@app.route('/recipes/<name>', methods=['DELETE'])
def delete_recipe(name):
    if client.delete(name):
        return jsonify({"message": "Recipe deleted successfully!"})
    else:
        return jsonify({"error": "Recipe not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)