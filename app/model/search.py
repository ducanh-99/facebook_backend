import mongoengine_goodjson as gj
from mongoengine import DateTimeField, ListField, ObjectIdField
import datetime


class Search(gj.Document):
    owner = ObjectIdField(required=True)
    history_search = ListField()

    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Search, self).save(*args, **kwargs)
