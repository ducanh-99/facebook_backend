from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from app.model.test import Test
from app.util.errors import InternalServerError

class TestApi(Resource):
    def get(self):
        query = Test.objects()
        test = Test.objects().to_json()
        return Response(test, mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            test = Test(**body)
            test.save()
            id = test.id
            return {'id' : str(id)}, 200
        except Exception as e:
            raise InternalServerError