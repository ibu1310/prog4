from flask import Flask, request, jsonify, render_template
import redis
import json

app = Flask(__name__)


client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def home():
    keys = client.keys()
    recipes = [{"name": key, **json.loads(client.get(key))} for key in keys]
    return render_template('index.html', recipes=recipes)

@app.route('/recipes/new', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        steps = request.form['steps']

        if not all([name, ingredients, steps]):
            return render_template('new_recipe.html', error="All fields are required.")

        recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        client.set(name, json.dumps(recipe))
        return render_template('success.html', message="Recipe added successfully!")

    return render_template('new_recipe.html')

@app.route('/recipes/<name>', methods=['GET', 'POST'])
def update_recipe(name):
    """Update an existing recipe."""
    recipe = client.get(name)
    if not recipe:
        return render_template('error.html', message="Recipe not found.")

    recipe_data = json.loads(recipe)
    if request.method == 'POST':
        ingredients = request.form.get('ingredients', recipe_data['ingredients'])
        steps = request.form.get('steps', recipe_data['steps'])

        updated_recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        client.set(name, json.dumps(updated_recipe))
        return render_template('success.html', message="Recipe updated successfully!")

    return render_template('edit_recipe.html', name=name, recipe=recipe_data)

@app.route('/recipes/<name>/delete', methods=['POST'])
def delete_recipe(name):
    if client.delete(name):
        return render_template('success.html', message="Recipe deleted successfully!")
    else:
        return render_template('error.html', message="Recipe not found.")

@app.route('/recipes/<name>')
def get_recipe(name):
    recipe = client.get(name)
    if recipe:
        recipe_data = json.loads(recipe)
        return render_template('view_recipe.html', name=name, recipe=recipe_data)
    else:
        return render_template('error.html', message="Recipe not found.")

if __name__ == '__main__':
    app.run(debug=True)
