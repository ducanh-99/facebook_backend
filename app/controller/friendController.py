from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.friends import Friend, Request
from app.model.user import User
import app.controller.responseController as resCon
import app.util.response as response

class RequestApi(Resource):
    res = {}
    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id) 
            owner = User.objects.get(id=id)
            # req = Request(owner=owner).save()
            request_friend = Request.objects.get(owner=owner)
            sent_request = Request.objects.get(owner=user)
            if user["id"] != owner["id"]:
                request_friend.request.append(user)
                sent_request.sent_request.append(owner)
            request_friend.save()
            sent_request.save()
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class RecommendFriendApi(Resource):
    pass

class ConfirmApi(Resource):
    res  = {}
    
    @jwt_required
    def get(self, id):
        try:
            owner_id = get_jwt_identity()
            owner = User.objects.get(id=owner_id)
            user = User.objects.get(id=id)
            # if user.friends == 0:
            #     friend = Friend(owner=user).save()
            request_owner = Request.objects.get(owner=owner)
            request_user = Request.objects.get(owner=user)

            friend_owner = Friend.objects.get(owner = owner)
            friend_user = Friend.objects.get(owner=user)

            if user["id"] != owner["id"]:
                friend_owner.friends.append(user)
                friend_user.friends.append(owner)
                owner.friends += 1
                user.friends += 1
            # save
            friend_owner.save()
            friend_user.save()
            owner.save()
            user.save()
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)

class BlockApi(Resource):
    pass

class ListBlockApi(Resource):
    pass


class ListFriendApi(Resource):
    pass

