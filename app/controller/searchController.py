from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.search import Search
from app.model.post import Post
import app.controller.responseController as resCon
import app.util.response as response


class SearchApi(Resource):
    res = {}

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            search = Search.objects(owner=user_id).first().to_json()
            return Response(search, mimetype="application/json", status=200)
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)
    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            # search_all = Search(owner=user_id).save()
            Search.objects(owner=user_id).update_one(push__history_search=body["keyword"])
            post = Post.objects(described__icontains = body["keyword"]).to_json()
            return Response(post, mimetype="application/json", status=200)
        except Exception:
            self.res = response.internal_server()
            # raise Exception
        return jsonify(self.res)
class ListSearchApi(Resource):
    pass
