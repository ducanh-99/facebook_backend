import mongoengine_goodjson as gj
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
from mongoengine import *
import uuid

from app.model.post import Post


class User(gj.Document):
    phonenumber = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    username = StringField(required=True)
    birthday = StringField(required=True)
    blocks = ListField(ReferenceField('User'))
    avatar = FileField(default=None)
    uuid = StringField(required=True)
    verify = BooleanField()
    posts = ListField(ReferenceField(
        'Post', reverse_delete_rule=PULL))
    friends = IntField(default=0)
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def default(self):
        self.username = self.firstname + " " + self.lastname
        self.uuid = str(uuid.uuid4())
        self.verify = False
        # self.blocks = []

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_uuid(self, uuid):
        return self.uuid == uuid

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)


User.register_delete_rule(Post, 'owner', CASCADE)
