import mongoengine_goodjson as gj
import mongoengine as mongo
import datetime


class Post(gj.Document):
    described = mongo.StringField(required=True)
    like = mongo.IntField(required=True)
    comment = mongo.IntField(required=True)
    is_liked = mongo.BooleanField()
    image = mongo.DictField()
    video = mongo.DictField()
    owner = mongo.ReferenceField('User')
    owner_avatar = mongo.StringField(required=True)
    owner_name = mongo.StringField(required=True)
    state = mongo.StringField()

    creation_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.datetime.now)

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
