
import mongoengine_goodjson as gj
import datetime
from mongoengine import ObjectIdField, StringField, IntField, EmbeddedDocumentField, ListField, LazyReferenceField, CASCADE, DateTimeField

from app.model.post import Post
from app.model.base_db import Base



class Content(gj.EmbeddedDocument):
    poster = ObjectIdField()
    poster_name = StringField()
    index = IntField()
    comment = StringField()
    created = DateTimeField(default=datetime.datetime.now)

class Comment(Base):
    post = LazyReferenceField(Post, reverse_delete_rule=CASCADE)
    content = ListField(EmbeddedDocumentField(Content))
    # creation_date = DateTimeField()
    # modified_date = DateTimeField(default=datetime.datetime.now)

    # def save(self, *args, **kwargs):
    #     if not self.creation_date:
    #         self.creation_date = datetime.datetime.now()
    #     self.modified_date = datetime.datetime.now()
    #     return super(Comment, self).save(*args, **kwargs)
    
    