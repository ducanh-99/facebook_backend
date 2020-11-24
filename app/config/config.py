from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


def config_everything(app):
    app.config['JWT_SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
    app.config['SECRET_KEY'] = 'secret!'
    Bcrypt(app)
    JWTManager(app)
