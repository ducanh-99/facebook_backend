import mongoengine_goodjson as gj
from mongoengine import FileField, StringField, IntField, EmbeddedDocumentField

from app.model.userEmbedd import UserEmbedd
from app.model.base_db import Base


class Images(gj.EmbeddedDocument):
    image1 = FileField(default=None)
    image2 = FileField(default=None)
    image3 = FileField(default=None)
    image4 = FileField(default=None)


class Post(Base):
    described = StringField(required=True)
    like = IntField(required=True, default=0)
    comment = IntField(required=True, default=0)
    images = EmbeddedDocumentField(Images)
    video = FileField(default=None)
    owner = EmbeddedDocumentField(UserEmbedd)
    state = StringField()
    

    def is_like(self, user_id):
        # like = Like.objects.get(post=self.id)
        pass



