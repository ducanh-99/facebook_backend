from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.post import Post
from app.model.user import User
import app.controller.responseController as resCon
import app.util.response as response

class RequestApi(Resource):
    pass

class RecommendFriendApi(Resource):
    pass

class ConfirmApi(Resource):
    pass

class BlockApi(Resource):
    pass

class ListBlockApi(Resource):
    pass


class ListFriendApi(Resource):
    pass

