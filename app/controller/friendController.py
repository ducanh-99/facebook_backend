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
            sender_id = get_jwt_identity()
            sender = User.objects.get(id=sender_id)
            recevied = User.objects.get(id=id)

            if sender["id"] != recevied["id"]:
                Friend.objects(owner=sender).update_one(
                    push__list_sent_request=recevied)
                Friend.objects(owner=recevied).update_one(
                    push__list_request=sender)

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
    res = {}

    @jwt_required
    def get(self, id):
        try:
            recevied_id = get_jwt_identity()
            recevied = User.objects.get(id=recevied_id)
            sender = User.objects.get(id=id)

            Friend.objects(owner=sender).update_one(
                pull__list_sent_request=recevied,
                push__list_friend=recevied,
                inc__friends=1)
            Friend.objects(owner=recevied).update_one(
                pull__list_request=sender,
                push__list_friend=sender,
                inc__friends=1)
            
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception

            self.res = response.internal_server()
        return jsonify(self.res)


class BlockApi(Resource):
    pass


class ListBlockApi(Resource):
    pass


class ListFriendApi(Resource):
    pass
