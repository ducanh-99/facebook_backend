from flask import Response, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist
import werkzeug
import os
import uuid
import json

from app.model.user import User
from app.model.friends import Friend
import app.util.response as response


class AvtUploadApi(Resource):
    decorators = []
    res = {}

    @jwt_required
    def post(self):
        try:
            body = request.files.get("file")
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            if body == "":
                return {
                    'data': '',
                    'message': 'No file found',
                    'status': 'error'
                }
            else:
                filename = str(uuid.uuid4().hex) + '.jpeg'
                user.avatar.replace(
                    body, content_type='image/jpeg', filename=filename)
                user.save()
                self.res = response.sucess()
                self.res["avatar"] = filename
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.upload_file_failed()
        return jsonify(self.res)


class AvatarApi(Resource):

    res = {}

    def get(self, id):
        try:
            user = User.objects.get(id=id)
            avatar = user.avatar.read()
            content_type = user.avatar.content_type
            return Response(avatar, content_type=content_type)
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)


class ProfileApi(Resource):
    res = {}

    @jwt_required
    def get(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            user = User.objects.get(id=user_id).to_json()
            user = json.loads(user)
            del user["password"]
            del user["blocks"]
            del user["uuid"]
            del user["verify"]
            if str(current_user_id) == str(user_id):
                pass
            user["is_friend"] = False
            current_friend = Friend.objects.get(owner=current_user_id)
            if current_friend.is_friend(user_id):
                user["is_friend"] = True
            self.res = user
        except DoesNotExist:
            self.res = response.user_is_invalid()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class UpdateProfileApi(Resource):

    @jwt_required
    def put(self):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            user = User.objects.get(id=current_user_id)
            body = request.get_json()
            if "firstname" in body:
                body["username"] = body["firstname"] + " " + user.lastname
            if "lastname" in body:
                body["username"] = user.firstname + " " + body["lastname"]
            user.update(**body)
            res = response.sucess()
        except DoesNotExist:
            res = response.user_is_invalid()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)
