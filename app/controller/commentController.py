from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.post import Post
from app.model.user import User
from app.model.comment import Comment, Content
import app.controller.responseController as resCon
import app.util.response as response


class PostCommentApi(Resource):
    res = {}
    @jwt_required
    def get(self, id):
        try:
            # prepare data
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            body = request.get_json()
            comment = Comment.objects.get(post=id)
            index = 0
            if 0 != len(comment.content):
                index = comment.content[-1]["index"] + 1
            content = Content(poster = user,index=index, comment=body["comment"])
            # save data
            comment.content.append(content)
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
            comment.save()
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            raise Exception
        return jsonify(self.res)
    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            comment = Comment.objects.get(post=id)
            for i in comment.content:
                if body["index"] == i["index"]:
                    comment.content.remove(i)
                    break
            comment.save()
            self.res = response.sucess()
            self.res["data"] = json.loads(comment.to_json())
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)




class SetCommentApi(Resource):
    pass
