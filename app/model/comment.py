
import mongoengine_goodjson as gj
import datetime
import mongoengine

class Comment(gj.Document):
    creation_date = mongoengine.DateTimeField()
    modified_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)