from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO

from app.routes.routes import initialize_routes
from app.util.errors import errors
from config import config
from app.routes import chat


app = Flask(__name__)
config(app)

app.register_blueprint(chat)
api = Api(app, errors=errors)
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


initialize_routes(api)
