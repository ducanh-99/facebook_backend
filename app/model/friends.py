
import mongoengine_goodjson as gj
import datetime
from mongoengine import *


class Friend(gj.Document):
    owner = ReferenceField('User')
    friends = ListField(ReferenceField('User'))
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
