import mongoengine_goodjson as gj
from mongoengine import *
import datetime

from app.model.image import Image
from app.model.video import Video


class Post(gj.Document):
    described = StringField(required=True)
    like = IntField(required=True)
    comment = IntField(required=True)
    is_liked = BooleanField()
    images = ListField(ReferenceField("Image"), reverse_delete_rule=PULL)
    video = ListField(ReferenceField('Video'), reverse_delete_rule=PULL)
    owner = ReferenceField('User')
    owner_avatar = StringField(required=True)
    owner_name = StringField(required=True)
    state = StringField()

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def set_default(self, user):
        self.like = 0
        self.comment = 0
        self.is_liked = False
        self.owner_name = user.username
        self.owner_avatar = user.avatar

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)

Post.register_delete_rule(Image, "post", CASCADE)
Post.register_delete_rule(Video, "post", CASCADE)
 