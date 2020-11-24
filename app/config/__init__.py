from .connect import connect_db
from .config import config_everything


def config(app):
    connect_db()
    config_everything(app)
