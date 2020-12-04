
import mongoengine_goodjson as gj
from mongoengine import IntField, ObjectIdField, ListField, EmbeddedDocumentField, StringField, DateTimeField
import datetime
from app.model.base_db import Base


class NotiContent(gj.EmbeddedDocument):
    index = IntField(default=1)
    text = StringField(required=True)
    user_id = ObjectIdField()
    username = StringField()
    post_id = ObjectIdField()
    read = IntField(default=0)
    create = DateTimeField(default=datetime.datetime.now)


class Notification(gj.Document):
    owner = ObjectIdField()
    content = ListField(EmbeddedDocumentField(NotiContent))

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Notification, self).save(*args, **kwargs)
    
    def read_notification(self, index):
        for i in range(len(self.content)):
            if index == self.content[i].index:
                self.content[i].read = 1
                return True
        return False

