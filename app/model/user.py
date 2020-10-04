import mongoengine_goodjson as gj
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
import mongoengine as mongo
import uuid

from app.model.post import Post


class User(gj.Document):
    phonenumber = mongo.StringField(required=True, unique=True)
    password = mongo.StringField(required=True, min_length=6)
    firtname = mongo.StringField(required=True)
    lastname = mongo.StringField(required=True)
    username = mongo.StringField(required=True)
    birthday = mongo.StringField(required=True)
    blocks = mongo.ListField(mongo.ReferenceField('User'))
    avatar = mongo.StringField()
    uuid = mongo.StringField(required=True)
    verify = mongo.BooleanField()
    posts = mongo.ListField(mongo.ReferenceField(
        'Post', reverse_delete_rule=mongo.PULL))
    creation_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.datetime.now)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def default(self):
        self.username = self.firtname + " " + self.lastname
        self.uuid = str(uuid.uuid4())
        self.avatar = "-1"
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


User.register_delete_rule(Post, 'owner', mongo.CASCADE)
