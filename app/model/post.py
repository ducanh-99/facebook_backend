import mongoengine_goodjson as gj
import datetime
from mongoengine import FileField, StringField, IntField, EmbeddedDocumentField,DateTimeField

from app.model.userEmbedd import UserEmbedd
from app.model.base_db import Base, pst_now


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
    modified_date = DateTimeField(default=pst_now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = pst_now
        self.modified_date = pst_now
        return super(Post, self).save(*args, **kwargs)

    def is_like(self, user_id):
        # like = Like.objects.get(post=self.id)
        pass
