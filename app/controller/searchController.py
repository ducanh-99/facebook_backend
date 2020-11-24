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
        result = []
        try:
            user_id = get_jwt_identity()
            search = Search.objects.get(owner=user_id)
            result = search.history_search

        except DoesNotExist:
            print("not search")
        except Exception:
            self.res = response.internal_server()
        return jsonify(result[::-1])
    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            search_all = Search.objects.get(owner=user_id)
            Search.objects(owner=user_id).update_one(push__history_search=body["keyword"])
            post = Post.objects(described__icontains = body["keyword"]).to_json()
            return Response(post, mimetype="application/json", status=200)
        except DoesNotExist:
            Search(owner=user_id).save()
        except Exception:
            self.res = response.internal_server()
            raise Exception
        return jsonify(self.res)
class ListSearchApi(Resource):
    pass
