from flask import Response, request
from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json


from app.model.test import Test, DocumentA, DocumentB
from app.model.user import User
from app.util.errors import InternalServerError
import app.util.response as response
from flask import jsonify

class TestApi(Resource):
    _res = {}
    def get(self):
        test = Test.objects().first()
        photo = test.test.read()
        content_type = test.test.content_type
        return Response(photo,content_type=content_type)

    # @jwt_required
    def post(self):
        try:
            # user_id = get_jwt_identity()
            body = request.files.get("file")
            print(body)
            # user = User.objects.get(id=user_id)
            test = Test()
            # test.default(user)
            test.test.put(body, content_type = 'image/jpeg',filename="test.jpeg")
            # id = test.id
            # self._res["id"] = str(id)
            test.save()
            self._res = response.sucess()
            return jsonify(self._res)
        except Exception as e:
            raise e

