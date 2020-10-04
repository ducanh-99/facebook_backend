import mongoengine_goodjson as gj
import datetime
import mongoengine


class Test(gj.Document):
    test = mongoengine.DictField()
    creation_date = mongoengine.DateTimeField()
    modified_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    def default(self, user):
        self.test["id"] = user.id
    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Test, self).save(*args, **kwargs)
