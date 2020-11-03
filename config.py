from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from mongoengine import connect


def config(app):
    app.config['JWT_SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
    Bcrypt(app)
    JWTManager(app)
    connect(
        db='fakebook',
        host='mongodb+srv://anhndvnist:ducanh99@cluster0.znpcr.mongodb.net'
    )
