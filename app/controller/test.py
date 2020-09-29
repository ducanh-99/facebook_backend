from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

class TestApi(Resource):
    def get(self):
        test = {
            "message" : "ok",
        }
        return Response(test, mimetype="application/json", status=200)