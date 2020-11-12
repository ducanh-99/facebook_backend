from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist


from app.model.post import Post
from app.model.like import Like
import app.controller.responseController as resCon
import app.util.response as response


class LikeApi(Resource):
    res = {}

    @jwt_required
    def get(self, id):
        try:
            # Check user was like
            user_id = get_jwt_identity()
            like = Like.objects.get(post=id)
            for i in like.user_like:
                if str(i["user"]) == user_id:
                    raise response.AlreadyLiked

            # get userEmbed
            user = resCon.convert_user_object_to_user_embed(user_id)
            like.update(push__user_like=user)

            # increase like
            post = Post.objects(id=id).first()
            post.update(inc__like=1)
            self.res = resCon.like_convert(post)
        except response.AlreadyLiked:
            self.res = response.user_was_like_post()
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            raise Exception
            self.res = response.internal_server()
        return jsonify(self.res)


class DislikeApi(Resource):
    res = {}
    check_user = False

    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            like = Like.objects.get(post=id)
            for userEmbed in like.user_like:
                if str(userEmbed["user"]) == user_id:
                    self.check_user = True
                    like.update(pull__user_like=userEmbed)
            
            if not self.check_user:
                raise Exception

            post = Post.objects(id=id).first()
            if post.like < 0:
                raise Exception
            post.update(dec__like=1)
            self.res = resCon.like_convert(post)
        except DoesNotExist:
            self.res = response.post_is_not_exit()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)
