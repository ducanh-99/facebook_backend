
import mongoengine_goodjson as gj
from mongoengine import IntField, ObjectIdField, ListField, EmbeddedDocumentField, StringField, DateTimeField
import datetime
from app.model.base_db import Base

class NotiContent(gj.EmbeddedDocument):
    text = StringField()
    user_id = ObjectIdField() 
    username = StringField()
    post_id = ObjectIdField()
    create = DateTimeField(default=datetime.datetime.now)

class Notification(gj.Document):
    owner = ObjectIdField()
    content  = ListField(EmbeddedDocumentField(NotiContent))

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Notification, self).save(*args, **kwargs)