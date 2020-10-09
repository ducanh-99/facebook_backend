import mongoengine_goodjson as gj
from mongoengine import *
import datetime

class Image(gj.Document):
    image = StringField()
    post = ReferenceField("Post")
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Image, self).save(*args, **kwargs)