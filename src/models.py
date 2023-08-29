from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)


    favorites = db.relationship("Favorites", backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "email": self.email

            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    homeworld = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)

    favorites = db.relationship("Favorites", backref='people', lazy=True)

    def __repr__(self):
        return f'<people {self.name}>' 

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "homeworld" : self.homeworld,
            "height" : self.height,
            "gender" : self.gender
        }

        
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(100), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=True, nullable=False)
    terrain = db.Column(db.String(100), unique=True, nullable=False)

    favorites = db.relationship("Favorites", backref='planet', lazy=True) 

    def __repr__(self):
        return f'<planet {self.name}>' 

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "climate" : self.climate,
            "population" : self.population,
            "terrain" : self.terrain
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), unique=False, nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), unique=False, nullable=True)




    def __repr__(self):
        return f'<favorite {self.id}>'

    def serialize(self):
        return {
            "id" : self.id,
            "user_id": self.user_id,
            "people_id" : self.people_id,
            "planet_id" : self.planet_id,
        }
