from flask import Flask
from flask_restful import Api

from app.routes.routes import initialize_routes
from app.util.errors import errors
from config import config


app = Flask(__name__)
config(app)

api = Api(app, errors=errors)

initialize_routes(api)