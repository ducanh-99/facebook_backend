from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.post import Post
from app.model.user import User
from app.model.like import Like
from app.model.comment import Comment
import app.controller.responseController as resCon
import app.util.response as response


def get_user_name(user):
    res = {
        "user": user["id"],
        "username": user["username"]
    }
    return res

def list_return(res, friend_anything):
    """
    docstring
    """
    data = []
    for i in friend_anything:
        data.append(resCon.convert_object_to_dict(i))
    res = response.sucess()
    res["data"] = data
    res["total"] = len(data)
    return res

class PostsApi(Resource):
    res = {}

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            posts = Post.objects()
            likes = Like.objects()
            # for i in len(posts):
            #     for j in likes[i]["user_like"]:
            #         print("ok")
            #         if user_id == j["user"]:
            #             print("ok")
                
            return Response(posts.to_json(), mimetype="application/json", status=200)
        except Exception :
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects(id=user_id).only('username').first()
            owner = get_user_name(user)
            post = Post(**body, owner=owner)
            post.save()
            Comment(post=post).save()
            return Response(post.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            self.res = response.user_is_not_validated()
        except Exception :
            raise e
            self.res = response.internal_server()
        return jsonify(self.res)


class PostApi(Resource):
    res = {}

    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            post = Post.objects.get(id=id)
            body = request.get_json()
            # post = resCon.update_post(post, body)
            # post["comment"] = 5
            post.update(**body)
            self.res = response.sucess()
            self.res = resCon.response_value(self.res, body)
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
            post = Post.objects(id=id).first()
            post.delete()
            self.res = response.sucess()
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        return jsonify(self.res)

    def get(self, id):
        try:
            post = Post.objects(id=id).first().to_json()
            self.res = response.sucess()
            self.res = resCon.format_response_post(self.res, post)
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)

class UserPostsApi(Resource):
    res = {}
    @jwt_required
    def get(self, user_id):
        try:
            posts = Post.objects()
            data = []
            for post in posts:
                if str(post.owner.user) == str (user_id):
                    data.append(resCon.convert_object_to_dict(post))
            return jsonify(data)
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)
        

        


class ReportPostApi(Resource):
    pass


class GetNewItemApi(Resource):
    pass
