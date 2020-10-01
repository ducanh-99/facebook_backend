from flask import Response, request
from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.test import Test
from app.util.errors import InternalServerError
import app.util.response as response
from flask import jsonify

class TestApi(Resource):
    _res = {}
    def get(self):
        query = Test.objects()
        test = Test.objects().to_json()
        self._res = response.sucess()
        self._res["data"] = {}
        test = json.loads(test)
        print (test[0])
        for i in test[0]:
            self._res["data"][i] = test[0][i]
        return jsonify(self._res)

    @jwt_required
    def post(self):
        try:
            # body = request.get_json()
            # test = Test(**body)
            # test.save()
            # id = test.id
            self._res["id"] = 'ok'
            return jsonify(self._res)
        except Exception as e:
            raise InternalServerError