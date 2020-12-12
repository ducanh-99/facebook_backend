from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.post import Post, Images
from app.model.user import User
from app.model.like import Like
from app.model.friends import Friend
from app.model.comment import Comment
from app.model.notification import Notification
import app.controller.responseController as resCon
import app.util.response as response


class Init(Resource):

    def get(self):
        self.notification()
        return "ok"

    def notification(self):
        users = json.loads(User.objects().to_json())
        for user in users:
            noti = Notification.objects(owner=user["id"]).first()
            if noti == None:
                print("test")
                Notification(owner=user["id"]).save()
