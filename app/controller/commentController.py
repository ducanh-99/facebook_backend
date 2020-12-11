from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import *
from bson.objectid import ObjectId
import json

from app.model.post import Post
from app.model.user import User
from app.model.comment import Comment, Content
import app.controller.responseController as resCon
import app.util.response as response
from app.controller.validation import is_block


class PostCommentApi(Resource):
    res = {}

    @jwt_required
    def get(self, post_id):
        try:
            comment = Comment.objects.get(post=post_id)
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)

    @jwt_required
    def post(self, post_id):
        try:
            # prepare data
            user_id = get_jwt_identity()
            post = Post.objects.get(id=post_id)
            is_block(user_id=user_id, other_user_id=post["owner"]["user"])

            body = request.get_json()
            user = User.objects.get(id=user_id)
            comment = Comment.objects.get(post=post_id)
            index = 0
            if 0 != len(comment.content):
                index = comment.content[-1]["index"] + 1
            content = Content(poster=user_id, index=index,
                              comment=body["comment"], poster_name=user.username)
            # save data
            comment.content.append(content)
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
            comment.save()
            post.update(inc__comment=1)
        except response.NotAccess:
            self.res = response.not_access()
        except ValidationError:
            self.res = response.parameter_value_invalid()
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            raise Exception
        return jsonify(self.res)

    @jwt_required
    def put(self, post_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            comment = Comment.objects.get(post=post_id)
            for i, value in enumerate(comment.content):
                if body["index"] == value["index"] and str(value["poster"]) == user_id:
                    comment.content[i]["comment"] = body["comment"]
                    break
            comment.save()
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)

    @jwt_required
    def delete(self, post_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            comment = Comment.objects.get(post=post_id)
            for i in comment.content:
                if body["index"] == i["index"] and str(i["poster"]) == user_id:
                    comment.content.remove(i)
                    break
            comment.save()
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
            Post.objects.get(id=post_id).update(dec__comment=1)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class SetCommentApi(Resource):

    @jwt_required
    def get(self, post_id):
        res = {}
        try:
            comment = Comment.objects.get(post=post_id)
            return Response(comment.to_json(), mimetype="application/json")
        except DoesNotExist:
            res = response.post_is_not_exit()
        except Exception:
            res = response.internal_server()
        return jsonify(res)
