
import mongoengine_goodjson as gj
import datetime
from mongoengine import * 

from app.model.post import Post



class Content(gj.EmbeddedDocument):
    poster = ReferenceField('User')
    index = IntField()
    comment = StringField()

class Comment(gj.Document):
    post = ReferenceField(Post, reverse_delete_rule=CASCADE)
    content = ListField(EmbeddedDocumentField(Content))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)