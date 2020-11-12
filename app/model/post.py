import mongoengine_goodjson as gj
from mongoengine import *
import datetime

from app.model.image import Image
from app.model.video import Video
from app.model.userEmbedd import UserEmbedd


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
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

    def is_like(self, user_id):
        # like = Like.objects.get(post=self.id)
        pass



Post.register_delete_rule(Image, "post", CASCADE)
Post.register_delete_rule(Video, "post", CASCADE)
