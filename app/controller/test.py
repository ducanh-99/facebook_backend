from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import inspect
import json

from app.model.test import Test
from app.util.errors import InternalServerError
import app.util.response as response
from flask import jsonify

class TestApi(Resource):
    _error = {}
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

    def post(self):
        try:
            body = request.get_json()
            test = Test(**body)
            test.save()
            id = test.id
            return {'id' : str(id)}, 200
        except Exception as e:
            raise InternalServerError