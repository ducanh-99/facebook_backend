import mongoengine_goodjson as gj
from mongoengine import *
import datetime

class Video(gj.Document):
    video = StringField()
    post = ReferenceField("Post")
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Video, self).save(*args, **kwargs)