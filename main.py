from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.model.db import initialize_db
from app.routes.routes import initialize_routes

app = Flask(__name__)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/test'
}

initialize_db(app)
initialize_routes(api)