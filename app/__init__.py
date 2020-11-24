from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO

# from .util.errors import errors
# from .config import config
# from .routes.routes import initialize_routes
# from .routes import chat

socketio = SocketIO()


def create_app(debug=False):
    from .util.errors import errors
    from .config import config
    from .routes.routes import initialize_routes
    from .chat import main as main_blueprint
    app = Flask(__name__)
    config(app)

    app.register_blueprint(main_blueprint)
    app.debug = debug
    api = Api(app, errors=errors)
    initialize_routes(api)

    socketio.init_app(app)

    return app
