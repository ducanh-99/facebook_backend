from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.friends import Friend
from app.model.user import User
import app.controller.responseController as resCon
import app.util.response as response


def get_user_name(user):
    res = {
        "user": user["id"],
        "username": user["username"]
    }
    return res


class RequestApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            sender_id = get_jwt_identity()
            recevied_id = id
            # Friend(owner=id).save()
            sender_friend = Friend.objects(owner=sender_id)
            for i in sender_friend.list_friend:
                if i["user"] == recevied_id:
                    raise response.AlreadyFriend
            sender = User.objects(id=sender_id).only('username').first()
            recevied = User.objects(id=recevied_id).only('username').first()

            sender_user = get_user_name(sender)
            recevied_user = get_user_name(recevied)

            if sender_id != recevied_id:
                Friend.objects(owner=sender_id).update_one(
                    push__list_sent_request=recevied_user, inc__sent_request=1)
                Friend.objects(owner=recevied_id).update_one(
                    push__list_request=sender_user, inc__requests=1)

            self.res = response.sucess()
        except response.AlreadyFriend:
            self.res = response.were_friend()
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class RecommendFriendApi(Resource):
    pass


class ConfirmApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            recevied_id = get_jwt_identity()
            sender_id = id
            # recevied = User.objects.get(id=recevied_id)
            # sender = User.objects.get(id=sender_id)
            if recevied_id != sender_id:
                sender_friend = Friend.objects(owner=sender_id).first()
                recevied_friend = Friend.objects(owner=recevied_id).first()
                for i in sender_friend.list_sent_request:
                    print(i["user"], recevied_id)
                    if str(i["user"]) == str(recevied_id):
                        sender_friend.update(
                            pull__list_sent_request=i,
                            push__list_friend=i,
                            dec__sent_request=1,
                            inc__friends=1
                        )
                for i in recevied_friend.list_request:
                    if str(i["user"]) == str(sender_id):
                        recevied_friend.update(
                            pull__list_request=i,
                            push__list_friend=i,
                            dec__requests=1,
                            inc__friends=1
                        )
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception

            self.res = response.internal_server()
        return jsonify(self.res)


class BlockApi(Resource):
    res = {}
    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            blocked_id = id
            if blocked_id != user_id:
                user_friend = Friend.objects(owner=user_id).first()
                blocked_friend = Friend.objects(owner=blocked_id).first()
                for i in user_friend.list_friend:
                    if str(i["user"]) == str(blocked_id):
                        user_friend.update()
                for i in blocked_friend.list_friend:
                    if str(i["user"]) == str(user_id):
                        blocked_friend.update()
            self.res = response.sucess()
            self.res["block_id"] = str(blocked_id) 
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)



class ListFriendApi(Resource):
    pass


class ListRequestApi(Resource):
    @jwt_required
    def get(self, id):
        user_id = get_jwt_identity()
        friend_request = Friend.objects.get(owner=user_id).list_request
        return jsonify(friend_request)


class ListBlockApi(Resource):
    pass
