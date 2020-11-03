import mongoengine_goodjson as gj
from mongoengine import *
import datetime

from app.model.userEmbedd import UserEmbedd

class Like(gj.Document):
    post = LazyReferenceField('Post', reverse_delete_rule=CASCADE)
    user_like = ListField()
