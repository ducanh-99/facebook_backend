import mongoengine_goodjson as gj
import mongoengine

class Posts(gj.Document):
    name = mongoengine.StringField(required=True, unique=True)
    casts = mongoengine.ListField(mongoengine.StringField(), required=True)
    genres = mongoengine.ListField(mongoengine.StringField(), required=True)
    added_by = mongoengine.ReferenceField('User')