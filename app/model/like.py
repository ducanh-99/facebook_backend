import mongoengine_goodjson as gj
from mongoengine import *
import datetime

from app.model.userEmbedd import UserEmbedd

class Like(gj.Document):
    post = LazyReferenceField('Post', reverse_delete_rule=CASCADE)
    user_like = ListField(EmbeddedDocumentField(UserEmbedd))

    def is_liked(self, user_id):
        for user in self.user_like:
            if str(user["user"]) == user_id:
                return True
        return False