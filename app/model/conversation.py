import mongoengine_goodjson as gj
import datetime
from mongoengine import EmbeddedDocumentField, ListField, ObjectIdField, StringField, DateTimeField
from app.model.base_db import Base

from .userEmbedd import UserEmbedd
from .user import User


class Message(gj.EmbeddedDocument):
    from_user = ObjectIdField()
    to_user = ObjectIdField()
    text = StringField()
    create = DateTimeField(default=datetime.datetime.now)


class Conversation(gj.Document):
    users = ListField(EmbeddedDocumentField(UserEmbedd))
    messages = ListField(EmbeddedDocumentField(Message))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Conversation, self).save(*args, **kwargs)

    def check_user(self, user_id):
        user = User.objects.get(id=user_id)
        for i in self.users:
            if str(i["user"]) == user_id:
                return True
        return False

    def check_list_user(self, list_user):
        return list_user == self.users or list_user[::-1] == self.users
