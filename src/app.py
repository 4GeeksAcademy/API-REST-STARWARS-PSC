"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# PEOPLE ENDPOINTS
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize()), 200
    return jsonify({"error": "Person not found"}), 404

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    name = data.get("name")
    height = data.get("height")
    gender = data.get("gender")

    if not name or not height or not gender:
        return jsonify({"error": "Missing required fields"}), 400

    new_person = People(name=name, height=height, gender=gender)
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 201

# PLANET ENDPOINTS
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"error": "Planet not found"}), 404

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    name = data.get("name")
    terrain = data.get("terrain")
    population = data.get("population")

    if not name or not terrain or not population:
        return jsonify({"error": "Missing required fields"}), 400

    new_planet = Planet(name=name, terrain=terrain, population=population)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

# USER ENDPOINTS
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  # Simulado (hasta que implementes autenticación)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites]), 200

# FAVORITE PLANET
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Simulado
    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"done": True}), 200
    return jsonify({"error": "Favorite not found"}), 404

# FAVORITE PEOPLE
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1
    new_fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"done": True}), 200
    return jsonify({"error": "Favorite not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
