"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites
#from models import Person

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

#endpoint user
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    serialize_user = [user.serialize() for user in users]
    if not users:
        return jsonify({"Error" : "No hay usuario"}), 404
    return jsonify({"Creando User" : serialize_user}), 200

@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json() 
    data_name = data.get("name", None)
    data_email = data.get("email", None)
    data_passw = data.get("password", None)
    #obtener los datos para crear el usuario
    #creando el nuevo usuario
    new_user = User(name=data_name, email=data_email,
    password=data_passw)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()),201

    except Exception as error:
        db.session.rollback()
        return error, 500



#endpoint favorites
@app.route('/favorites', methods=['GET'])
def get_user_and_favorite():

    get_favorite = Favorites.query.all()
    serialize_favorite = [favorite.serialize() for favorite in get_favorite]
    if not get_favorite:
        return jsonify({"Error" : "No tienes favoritos"}), 404
    return jsonify({"Felicidades" : serialize_favorite}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorite(planet_id):

    data = request.get_json()
    data_user_id = data.get("user_id", None)
    new_favorite = Favorites(user_id =data_user_id,  planet_id=planet_id)

    try:
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()),201

    except Exception as error:
        db.session.rollback()
        return jsonify(error), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorite(people_id):

    data = request.get_json()
    people_user_id = data.get("user_id", None)
    people_favorite = Favorites(user_id =people_user_id,  people_id=people_id)

    try:
        db.session.add(people_favorite)
        db.session.commit()
        return jsonify(people_favorite.serialize()),201

    except Exception as error:
        db.session.rollback()
        return jsonify(error), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet_to_delete = Favorite.query.get(planet_id)
    if not planet_to_delete:
        if not planet_to_delete:
            return jsonify({"Error": "Planet not found"}), 404

    try:
        db.session.delete(planet_to_delete)
        db.session.commit()    
        return jsonify(planet_to_delete.serialize()), 200  
    except Exception as error:
        db.session.rollback()
        return error, 500
    


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):

    people_to_delete = Favorite.query.get(people_id)
    if not people_to_delete:
        if not people_to_delete:
            return jsonify({"Error": "Planet not found"}), 404

    try:
        db.session.delete(people_to_delete)
        db.session.commit()    
        return jsonify(people_to_delete.serialize()), 200  
    except Exception as error:
        db.session.rollback()
        return error, 500


#endpoint de people 
@app.route('/people', methods=['GET'])
def get_people():
    
    get_people = People.query.all()
    serialize_people = [people.serialize() for people in get_people]
    if not get_people:
        return jsonify({"Error": "No hay people"}), 404
    return jsonify({"Creando People" : serialize_people}), 200


#endpoint peopleid
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    people_id = People.query.get(people_id)
    if not people_id:
        return jsonify({"Error": "People not found"}), 404
    return jsonify(people_id.serialize()),200


#endpoint planet
@app.route('/planet', methods=['GET'])
def get_planet():

    planets = Planet.query.all()
    serialize_planet = [planet.serialize() for planet in planets]
    if not planets:
        return jsonify({"Eror": "No hay planeta"}), 404
    return jsonify({"Creando Planeta" : serialize_planet}), 200


#endpoint planetid
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):

    planets_id = Planet.query.get(planet_id)
    if not planets_id:
        return jsonify({"Error": "No hay planeta"}), 404
    return jsonify(planets_id.serialize()), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

