
import mongoengine_goodjson as gj
import datetime
from mongoengine import *


class UserEmbedd(gj.EmbeddedDocument):
    user = ReferenceField('User')


class Friend(gj.Document):
    owner = ReferenceField('User')
    friends = IntField(default=0)
    list_friend = ListField(ReferenceField('User'))
    requests = IntField(default=0)
    list_request = ListField(ReferenceField('User'))
    list_sent_request = ListField(ReferenceField('User'))
    blocks = IntField(default=0)
    list_block = ListField(ReferenceField('User'))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Friend, self).save(*args, **kwargs)


class Request(gj.Document):
    owner = ReferenceField('User', reverse_delete_rule=CASCADE)
    request = ListField(ReferenceField('User'))
    sent_request = ListField(ReferenceField('User'))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Request, self).save(*args, **kwargs)
