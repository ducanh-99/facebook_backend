import mongoengine_goodjson as gj
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
import mongoengine
import uuid


class User(gj.Document):
    phonenumber = mongoengine.StringField(required=True, unique=True)
    password = mongoengine.StringField(required=True, min_length=6)
    username = mongoengine.StringField(required=True)
    avatar = mongoengine.StringField()
    uuid = mongoengine.StringField(required=True)
    verify = mongoengine.BooleanField()
    creation_date = mongoengine.DateTimeField()
    modified_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')


    def default(self):
        self.uuid = str(uuid.uuid4())
        self.avatar = "-1"
        self.verify = False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_uuid(self, uuid):
        return self.uuid == uuid

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)
