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
    res["text"] = text
    for i in kwargs:
        res[i] = kwargs[i]
    return res


class NotificationsApi(Resource):

    @jwt_required
    def get(self):
        res = {}

        try:
            current_user_id = get_jwt_identity()
            notifications = json.loads(
                Notification.objects.get(owner=current_user_id).to_json())

            res =  notifications
        except DoesNotExist:
            res = response.user_is_invalid()
        return jsonify(res)
    
    @jwt_required
    def post(self):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            body = request.get_json()
            noti = Notification.objects.get(owner=current_user_id)
            noti.read_notification(index=body["index"])
            noti.save()
        except DoesNotExist:
            res = response.post_is_not_exit()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)
    
class NotificationApi(Resource):

    @jwt_required
    def get(self, noti_id):
        res = {}
        try:
            body = request.get_json()
            noti = Notification.objects.get(id=noti_id)
            noti.read_notification(index=body["index"])
            noti.save()
        except DoesNotExist:
            res = response.post_is_not_exit()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)
        


class NotificationController():

    def like(self, owner, user_id, username, post_id):
        content = {}
        try:
            notification = Notification.objects.get(owner=owner)
            index = notification.content[-1].index + 1
            print(index)

            text = str(username) + " đã thích bài viết của bạn"
            content = set_content(text=text, user_id=user_id,
                                  post_id=post_id, username=username, index=index)
            print(content)
            notification.update(push__content=content)
        except DoesNotExist:
            Notification(owner=owner).save()

    def comment(self, owner, user_id, username, post_id):
        try:
            notification = Notification.objects.get(owner=owner)

            text = str(username) + " đã bình luận bài viết của bạn"
            content = set_content(text=text, user_id=user_id,
                                  post_id=post_id, username=username)
            print(content)
            notification.update(push__content=content)
        except DoesNotExist:
            Notification(owner=owner).save()

    def friend_new_post(self, username):
        return str(username) + " đã đăng một bài viết mới"

    def friend_request(self, owner, user_id, username):
        try:
            notification = Notification.objects.get(owner=owner)
            text = str(username) + " đã gửi lời mới kết bạn"
            content = set_content(
                text=text, user_id=user_id, username=username)
            notification.update(push__content=content)
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
