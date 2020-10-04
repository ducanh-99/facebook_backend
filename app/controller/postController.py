from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from app.model.post import Post
from app.model.user import User
import app.controller.responseController as resCon
import app.util.response as response


class PostsApi(Resource):
    res = {}

    def get(self):
        try:
            query = Post.objects()
            posts = Post.objects().to_json()
            return Response(posts, mimetype="application/json", status=200)
        except Exception as e:
            self.res = response.internal_server()
            return jsonify(self.res)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            post = Post(**body, owner=user)
            post.set_default(user)
            post.save()
            user.update(push__posts=post)
            return {"mes": "ok"}, 200
        except DoesNotExist:
            self.res = response.user_is_not_validated()
        except Exception as e:
            self.res = response.internal_server()
        return jsonify(self.res)


class PostApi(Resource):
    res = {}

    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            post = Post.objects.get(id=id, owner=user_id)
            body = request.get_json()
            Post.objects.get(id=id).update(**body)
            self.res = response.sucess()
            self.res = resCon.format_response_post(self.res, body)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception as e:
            raise e
            self.res = response.internal_server()
        return jsonify(self.res)

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            post = Post.objects.get(id=id, owner=user_id)
            post.delete()
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        return jsonify(self.res)

    def get(self, id):
        try:
            post = Post.objects.get(id=id).to_json()
            self.res = response.sucess()
            self.res = resCon.format_response_post(self.res, post)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception as e:
            self.res = response.internal_server()
        return jsonify(self.res)
