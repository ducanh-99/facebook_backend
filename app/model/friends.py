
import mongoengine_goodjson as gj
import datetime
from mongoengine import ObjectIdField, StringField, IntField, ListField, EmbeddedDocumentField, DateTimeField


class UserEmbedd(gj.EmbeddedDocument):
    user = ObjectIdField()
    username = StringField()


class Friend(gj.Document):
    owner = ObjectIdField(required=True)
    friends = IntField(default=0)
    list_friend = ListField(EmbeddedDocumentField(UserEmbedd))
    requests = IntField(default=0)
    list_request = ListField(EmbeddedDocumentField(UserEmbedd))
    sent_request = IntField(default=0)
    list_sent_request = ListField(EmbeddedDocumentField(UserEmbedd))
    blocks = IntField(default=0)
    list_block = ListField(EmbeddedDocumentField(UserEmbedd))
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Friend, self).save(*args, **kwargs)

    def find_user(self, a_list, user_id):
        for i in a_list:
            if str(i["user"]) == str(user_id):
                return True
        return False

    def is_blocked(self, user_id):
        return self.find_user(a_list=self.list_block, user_id=user_id)

    def is_friend(self, user_id):
        return self.find_user(a_list=self.list_friend, user_id=user_id)

    def is_request(self, user_id):
        return self.find_user(a_list=self.list_request, user_id=user_id)    

    def is_sent_request(self, user_id):
        return self.find_user(a_list=self.list_sent_request, user_id=user_id)    

    def reject_request_recevied(self, user_id):
        for i in self.list_request:
            if str(i["user"]) == str(user_id):
                self.update(
                    pull__list_request=i,
                    dec__requests=1,
                )

    def reject_request_sender(self, user_id):
        for i in self.list_sent_request:
            if str(i["user"]) == str(user_id):
                self.update(
                    pull__list_sent_request=i,
                    dec__sent_request=1,
                )
    
    def common_friend(self, user_id):
        friend = self.objects.get(owner=user_id)
        return "ok"
