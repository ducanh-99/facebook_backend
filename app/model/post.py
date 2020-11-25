import mongoengine_goodjson as gj
import datetime
from mongoengine import FileField, StringField, IntField, EmbeddedDocumentField,DateTimeField

from app.model.userEmbedd import UserEmbedd
from app.model.base_db import Base, d_aware


class Images(gj.EmbeddedDocument):
    image1 = FileField(default=None)
    image2 = FileField(default=None)
    image3 = FileField(default=None)
    image4 = FileField(default=None)


class Post(gj.Document):
    described = StringField(required=True)
    like = IntField(required=True, default=0)
    comment = IntField(required=True, default=0)
    images = EmbeddedDocumentField(Images)
    video = FileField(default=None)
    owner = EmbeddedDocumentField(UserEmbedd)
    state = StringField()

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=d_aware)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = d_aware
        self.modified_date = d_aware
        return super(Post, self).save(*args, **kwargs)

    def is_like(self, user_id):
        # like = Like.objects.get(post=self.id)
        pass
