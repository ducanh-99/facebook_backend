
import mongoengine_goodjson as gj
from mongoengine import IntField
from app.model.base_db import Base


class Setting(Base):
    like_comment = IntField(default=1)
    from_friends = IntField(default=1)
    request_friends = IntField(default=1)
    suggested_friend = IntField(default=1)
    birthday = IntField(default=1)
    video = IntField(default=1)
    report = IntField(default=1)
    sound_on = IntField(default=1)
    notification_on = IntField(default=1)
    vibrant_on = IntField(default=1)
    led_on = IntField(default=1)
