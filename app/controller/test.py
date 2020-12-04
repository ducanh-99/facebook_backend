from flask import Response, request, session
from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json


from app.model.test import Test, DocumentA, DocumentB
from app.model.user import User
from app.model.post import Post
from ..model.friends import Friend
from app.util.errors import InternalServerError
import app.util.response as response
from flask import jsonify

class TestApi(Resource):
    _res = {}
    def get(self):
        # test = Test.objects().first()
        # photo = test.test.read()
        # print(photo)
        # content_type = test.test.content_type
        # return Response(photo,content_type=content_type)
        # posts = Post.objects()
        # friend = Friend.objects.get(id = '5fa2409eae3837c3b38cc8d5')
        # friend.common_friend("5fa41398638526ffe8979a33")
        res = []
        for i in session:
            res.append(i)
            print(i)
        res.append(session["room"])
        return Response(res, mimetype="application/json")

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

