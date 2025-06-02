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
from models import db, User, People, Planet, Favorite  # Asegúrate de que los modelos estén correctamente definidos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'  # Cambia esto si usas otra DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

# --------------------- PEOPLE ---------------------

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify({
        "success": True,
        "message": "Lista completa de personajes",
        "data": [p.serialize() for p in people]
    }), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({
            "success": True,
            "message": f"Personaje con ID {people_id} encontrado",
            "data": person.serialize()
        }), 200
    return jsonify({
        "success": False,
        "message": f"No se encontró personaje con ID {people_id}",
        "error": "Not Found"
    }), 404

# --------------------- PLANETS ---------------------

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify({
        "success": True,
        "message": "Lista completa de planetas",
        "data": [p.serialize() for p in planets]
    }), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({
            "success": True,
            "message": f"Planeta con ID {planet_id} encontrado",
            "data": planet.serialize()
        }), 200
    return jsonify({
        "success": False,
        "message": f"No se encontró planeta con ID {planet_id}",
        "error": "Not Found"
    }), 404

# --------------------- USERS ---------------------

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify({
        "success": True,
        "message": "Lista de usuarios",
        "data": [u.serialize() for u in users]
    }), 200

# --------------------- FAVORITES ---------------------

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  # Simulado por ahora
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify({
        "success": True,
        "message": f"Favoritos del usuario con ID {user_id}",
        "data": [f.serialize() for f in favorites]
    }), 200

# Agregar favorito - PLANETA
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Simulado
    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Planeta con ID {planet_id} agregado a favoritos",
        "data": new_fav.serialize()
    }), 201

# Agregar favorito - PERSONAJE
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  # Simulado
    new_fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Personaje con ID {people_id} agregado a favoritos",
        "data": new_fav.serialize()
    }), 201

# Eliminar favorito - PLANETA
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Favorito planeta ID {planet_id} eliminado"
        }), 200
    return jsonify({
        "success": False,
        "message": f"Favorito planeta ID {planet_id} no encontrado",
        "error": "Not Found"
    }), 404

# Eliminar favorito - PERSONAJE
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1
    fav = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Favorito personaje ID {people_id} eliminado"
        }), 200
    return jsonify({
        "success": False,
        "message": f"Favorito personaje ID {people_id} no encontrado",
        "error": "Not Found"
    }), 404

# --------------------- MAIN ---------------------


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
