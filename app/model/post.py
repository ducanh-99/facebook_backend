import mongoengine_goodjson as gj
from mongoengine import *
import datetime

from app.model.image import Image
from app.model.video import Video
from app.model.userEmbedd import UserEmbedd


class Post(gj.Document):
    described = StringField(required=True)
    like = IntField(required=True, default=0)
    comment = IntField(required=True, default=0)
    is_liked = BooleanField(default=False)
    images = ListField(FileField())
    video = ListField(FileField())
    owner = EmbeddedDocumentField(UserEmbedd)
    state = StringField()

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

Post.register_delete_rule(Image, "post", CASCADE)
Post.register_delete_rule(Video, "post", CASCADE)
 