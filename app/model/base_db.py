from mongoengine import DateField
import mongoengine_goodjson as gj 
import datetime

class Base(gj.Document):
    meta = {'abstract': True}
    creation_date = DateField()
    modified_date = DateField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Base, self).save(*args, **kwargs)
    
