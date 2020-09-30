from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

def config(app):
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    DB_URI = 'mongodb+srv://anhndvnist:ducanh99@cluster0.znpcr.mongodb.net/fakebook?retryWrites=true&w=majority'
    app.config['MONGODB_SETTINGS'] = {
        "host" : DB_URI
    }