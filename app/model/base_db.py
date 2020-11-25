from mongoengine import DateField
import mongoengine_goodjson as gj 
import datetime
import pytz
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("Asia/Vientiane"))

class Base(gj.Document):
    meta = {'abstract': True}
    creation_date = DateField()
    modified_date = DateField(default=pst_now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = pst_now
        self.modified_date = pst_now
        return super(Base, self).save(*args, **kwargs)
    
