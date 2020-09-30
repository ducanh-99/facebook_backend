from flask_mongoengine import MongoEngine


def initialize_db(app):
    db = MongoEngine(app)