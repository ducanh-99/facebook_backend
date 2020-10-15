import mongoengine_goodjson as gj
import datetime
from mongoengine import *


class UserEmbedd(gj.EmbeddedDocument):
    user = ObjectIdField()
    username = StringField()