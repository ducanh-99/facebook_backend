from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.friends import Friend
from app.model.user import User
from app.model.userEmbedd import UserEmbedd
import app.controller.responseController as resCon
import app.util.response as response


def get_user_name(user):
    res = {
        "user": user["id"],
        "username": user["username"]
    }
    return res


def list_return(res, friend_anything):
    """
    docstring
    """
    data = []
    for i in friend_anything:
        data.append(resCon.convert_object_to_dict(i))
    res = response.sucess()
    res["data"] = data[::-1]
    res["total"] = len(data)
    return res


class RequestApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            sender_id = get_jwt_identity()
            recevied_id = id
            # Friend(owner=id).save()
            sender_friend = Friend.objects(owner=sender_id).first()
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

    @jwt_required
    def get(self):
        res = []
        try:
            # init
            current_user_id = get_jwt_identity()
            current_friend = json.loads(
                Friend.objects.get(owner=current_user_id).to_json())
            friends = json.loads(Friend.objects.to_json())

            for friend in friends:
                common = self.common_friend(current_friend, friend)
                user = self.get_owner_name(friend["owner"])
                user["common_friend"] = common
                res.append(user)
        except DoesNotExist:
            res = response.user_is_invalid()
        return jsonify(res)

    def common_friend(self, current_friend, friend):
        count = 0
        for i in current_friend["list_friend"]:
            if i in friend["list_friend"]:
                count += 1
        return count

    def get_owner_name(self, user_id):
        user = json.loads(User.objects.get(id=user_id).to_json())
        return get_user_name(user)


class ConfirmApi(Resource):
    res = {}
    check_request = False

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
                    if str(i["user"]) == str(recevied_id):
                        sender_friend.update(
                            pull__list_sent_request=i,
                            push__list_friend=i,
                            dec__sent_request=1,
                            inc__friends=1
                        )
                        self.check_request = True
                for i in recevied_friend.list_request:
                    if str(i["user"]) == str(sender_id):
                        recevied_friend.update(
                            pull__list_request=i,
                            push__list_friend=i,
                            dec__requests=1,
                            inc__friends=1
                        )
                        self.check_request = True
            if self.check_request:
                self.res = response.sucess()
            else:
                raise Exception
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)


class RejectApi(Resource):

    @jwt_required
    def post(self, sender_id):
        res = {}
        try:
            recevied_id = get_jwt_identity()
            if recevied_id != sender_id:
                sender_friend = Friend.objects(owner=sender_id).first()
                recevied_friend = Friend.objects(owner=recevied_id).first()
                sender_friend.reject_request_sender()
                recevied_friend.reject_request_recevied()
        except Exception:
            res = response.internal_server()
        return jsonify(res)


class BlockApi(Resource):
    res = {}

    @jwt_required
    def get(self, block_id):
        try:
            user_id = get_jwt_identity()
            if block_id != user_id:
                user = User.objects(id=user_id).only('username').first()
                blocker = User.objects(id=block_id).only('username').first()
                if user == None:
                    raise DoesNotExist
                if blocker == None:
                    raise DoesNotExist

                user_friend = Friend.objects.get(owner=user_id)
                blocker_friend = Friend.objects.get(owner=block_id)
                blocker_embedded = get_user_name(blocker)
                if user_friend.is_friend(block_id):
                    user_friend.update(pull__list_friend=i, dec__friends=1)

                if blocker_friend.is_friend(user_id):
                    blocker_friend.update(pull__list_friend=i, dec__friends=1)
                user_friend.update(
                    push__list_block=blocker_embedded, inc__blocks=1)
            self.res = response.sucess()
            self.res["block_id"] = str(block_id)
        except DoesNotExist:
            self.res = response.user_is_not_validated()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)


class ListFriendApi(Resource):
    res = {}

    def get(self, user_id):
        try:
            list_friend = Friend.objects.get(owner=user_id).list_friend
            self.res = list_return(self.res, list_friend)
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)


class ListRequestApi(Resource):
    res = {}

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            list_request = Friend.objects.get(owner=user_id).list_request
            self.res = list_return(self.res, list_request)
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class ListSentRequestApi(Resource):
    res = {}

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            list_sent_request = Friend.objects.get(
                owner=user_id).list_sent_request
            self.res = list_return(self.res, list_sent_request)
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class ListBlockApi(Resource):
    res = {}

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            list_block = Friend.objects.get(owner=user_id).list_block
            self.res = list_return(self.res, list_block)
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)
