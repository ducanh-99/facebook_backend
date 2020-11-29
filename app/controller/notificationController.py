from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.notification import Notification, NotiContent
from ..model.user import User
import app.controller.responseController as resCon
import app.util.response as response


def set_content(text, **kwargs):
    res = {}
    for i in kwargs:
        res[i] = kwargs[i]
    return res

class NotificationController():


    def like(self, owner, user_id, username, post_id, ):
        content = {}
        try: 
            notification = Notification.objects.get(owner=owner)

            text = str(username) + " đã thích bài viết của bạn"
            content = set_content(text=text, user_id=user_id, post_id=post_id, username=username)
            notification.update(push__content = content)
        except DoesNotExist:
            Notification(owner=owner).save()

    def comment(self, username):
        return str(username) + " đã bình luận bài viết của bạn"

    def friend_new_post(self, username):
        return str(username) + " đã đăng một bài viết mới"

    def friend_request(self,owner, user_id, username):
        try: 
            notification = Notification.objects.get(owner=owner)
            text = str(username) + " đã gửi lời mới kết bạn"
            content = set_content(text=text, user_id=user_id, username=username)
            notification.update(push__content = content)
        except DoesNotExist:
            Notification(owner=owner).save()

    def friend_recommend(self, username):
        return "Bạn có một gợi ý kết bạn mới " + str(username)

    def birthday(self, username):
        return "Hôm nay là sinh nhât" + str(username)

    def report_post(self):
        return "Báo cáo bài viết của bạn đã được phản hooif"

    def login_other(self):
        return "Có người đã đăng nhập vào tài khoản của bạn"


