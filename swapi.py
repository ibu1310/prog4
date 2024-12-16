from flask import Flask, jsonify
import requests

app = Flask(__name__)

SWAPI_BASE_URL = "https://swapi.dev/api/"

def get_movies():
    response = requests.get(SWAPI_BASE_URL + "films/")
    return response.json().get('results', [])

def get_planets():
    response = requests.get(SWAPI_BASE_URL + "planets/")
    return response.json().get('results', [])

def get_characters():
    response = requests.get(SWAPI_BASE_URL + "people/")
    return response.json().get('results', [])

def get_ships():
    response = requests.get(SWAPI_BASE_URL + "starships/")
    return response.json().get('results', [])

@app.route('/arid-planets-movies', methods=['GET'])
def arid_planets_movies():
    movies = get_movies()
    planets = get_planets()
    

    arid_planet_names = [planet['name'] for planet in planets if 'arid' in planet.get('climate', '').lower()]
    
    count = 0
    for movie in movies:
        for planet_url in movie.get('planets', []):
            if planet_url in [planet['url'] for planet in planets if 'arid' in planet.get('climate', '').lower()]:
                count += 1
                break
    
    return jsonify({"arid_planets_movie_count": count})


@app.route('/total-wookies', methods=['GET'])
def total_wookies():
    characters = []
    url = SWAPI_BASE_URL + "people/"
    
    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data.get('results', []))
        url = data.get('next')
  
    wookie_count = sum(1 for character in characters if 'wookie' in character.get('species', [])[0].lower())
    
    return jsonify({"total_wookies": wookie_count})


@app.route('/smallest-ship-first-movie', methods=['GET'])
def smallest_ship_first_movie():
    
    movies = get_movies()
    first_movie_url = movies[0]['url']
    
    response = requests.get(first_movie_url)
    ships_urls = response.json().get('starships', [])
    
    ships = []
    for ship_url in ships_urls:
        ship_response = requests.get(ship_url)
        ship_data = ship_response.json()
        ships.append({
            "name": ship_data.get('name'),
            "length": float(ship_data.get('length', '0')) if ship_data.get('length') else float('inf')
        })
  
    ships_sorted = sorted(ships, key=lambda x: x['length'] if x['length'] < float('inf') else float('inf'))
    
    smallest_ship = next((ship for ship in ships_sorted if ship['length'] != float('inf')), None)
    
    return jsonify({"smallest_ship": smallest_ship.get('name') if smallest_ship else None})


if __name__ == '__main__':
    app.run(debug=True)
