import mongoengine_goodjson as gj
import datetime
from mongoengine import EmbeddedDocumentField, ListField, ObjectIdField, StringField, DateTimeField, IntField
from app.model.base_db import Base

from .userEmbedd import UserEmbedd
from .user import User


class Message(gj.EmbeddedDocument):
    from_user = ObjectIdField()
    to_user = ObjectIdField()
    text = StringField()
    create = DateTimeField(default=datetime.datetime.now)
    index = IntField()


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

    def get_index(self):
        index = 1
        if len(self.messages) != 0:
            index = self.messages[-1].index + 1
        return index

    def get_other_user(self, user_id):
        other_user_id = ""
        for user in self.users:
            other_user_id = str(user["user"])
            if other_user_id != user_id:
                return other_user_id
    
    def get_message_by_index(self, index):
        for message in self.messages:
            if index == message["index"]:
                return message
        return None

