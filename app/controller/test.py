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
        self.res = response.sucess()
        return jsonify(self._res)

    # @jwt_required
    def post(self):
        try:
            # user_id = get_jwt_identity()
            body = request.get_json()
            # user = User.objects.get(id=user_id)
            test = DocumentB()
            # test.default(user)
            test.save(**body)
            id = test.id
            self._res["id"] = str(id)
            return jsonify(self._res)
        except Exception as e:
            raise e

