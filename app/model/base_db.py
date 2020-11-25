from mongoengine import DateField
import mongoengine_goodjson as gj 
import datetime
import pytz
d = datetime.datetime.now()
timezone = pytz.timezone("Asia/Vientiane")
d_aware = timezone.localize(d)

class Base(gj.Document):
    meta = {'abstract': True}
    creation_date = DateField()
    modified_date = DateField(default=d_aware)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = d_aware
        self.modified_date = d_aware
        return super(Base, self).save(*args, **kwargs)
    
