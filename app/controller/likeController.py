from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist


from app.model.post import Post
import app.controller.responseController as resCon
import app.util.response as response


class LikeApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            post = Post.objects.get(id=id)
            post.like += 1
            post.save()
            self.res = resCon.like_convert(post)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)


class DislikeApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            post = Post.objects.get(id=id)
            post.like -= 1
            if post.like < 0:
                raise Exception
            post.save()
            self.res = resCon.like_convert(post)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)
